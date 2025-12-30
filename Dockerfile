# ---
# Build arguments
# ---
ARG DOCKER_PARENT_IMAGE=nixos/nix:latest
FROM $DOCKER_PARENT_IMAGE

# NB: Arguments should come after FROM otherwise they're deleted
ARG BUILD_DATE
ARG PROJECT_NAME

# ---
# Environment variables
# ---
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8
ENV TZ=Australia/Sydney
ENV HOME=/home/$PROJECT_NAME

LABEL org.label-schema.build-date=$BUILD_DATE \
    maintainer="Humberto STEIN SHIROMOTO <hsteinshiromoto@gmail.com>"

# ---
# Create home directory and set workdir
# ---
RUN mkdir -p $HOME && mkdir -p $HOME/gems
WORKDIR $HOME

# ---
# Configure Nix
# ---
RUN echo "experimental-features = nix-command flakes" >> /etc/nix/nix.conf

# ---
# Install system packages via Nix
# ---
RUN nix-env -iA \
    nixpkgs.ruby \
    nixpkgs.nodejs \
    nixpkgs.stdenv.cc \
    nixpkgs.gnumake

# Set up Nix environment in shell initialization
RUN echo '. /root/.nix-profile/etc/profile.d/nix.sh' >> /root/.bashrc && \
    echo '. /root/.nix-profile/etc/profile.d/nix.sh' >> /root/.profile

# Add Nix profiles to PATH for non-interactive shells
ENV PATH="/nix/var/nix/profiles/per-user/root/profile/bin:/root/.nix-profile/bin:${PATH}"

# Install bundler via gem to a known location
ENV GEM_HOME="/usr/local/bundle"
ENV PATH="/usr/local/bundle/bin:${PATH}"
RUN export PATH="/nix/var/nix/profiles/per-user/root/profile/bin:$PATH" && gem install bundler

# ---
# Configure timezone
# ---
RUN ln -sf /nix/store/$(ls /nix/store | grep -m1 "tzdata.*")/share/zoneinfo/$TZ /etc/localtime

# ---
# Install Ruby Gems
# ---

# Prepare to install ruby packages into container
COPY Gemfile minimal-mistakes-jekyll.gemspec $HOME/gems/

RUN export PATH="/nix/var/nix/profiles/per-user/root/profile/bin:$PATH" && cd $HOME/gems && bundle install

# Copy and set up entrypoint script
COPY bin/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# ---
# Expose Jekyll port
# ---
EXPOSE 4000

# ---
# Set entrypoint and default command
# ---
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0"]
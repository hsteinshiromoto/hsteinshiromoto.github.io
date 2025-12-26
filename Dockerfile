# ---
# Build arguments
# ---
ARG DOCKER_PARENT_IMAGE=nixos/nix:latest
FROM $DOCKER_PARENT_IMAGE

# NB: Arguments should come after FROM otherwise they're deleted
ARG BUILD_DATE
ARG PROJECT_NAME
ARG PYTHON_VERSION=3.11

# ---
# Environment variables
# ---
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8
ENV TZ=Australia/Sydney
ENV HOME=/home/$PROJECT_NAME
ENV PYTHON_VERSION=$PYTHON_VERSION
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false

LABEL org.label-schema.build-date=$BUILD_DATE \
    maintainer="Humberto STEIN SHIROMOTO <h.stein.shiromoto@gmail.com>"

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
    nixpkgs.ruby_3_2 \
    nixpkgs.bundler \
    nixpkgs.python311 \
    nixpkgs.python311Packages.pip \
    nixpkgs.poetry \
    nixpkgs.git \
    nixpkgs.gitAndTools.git-flow \
    nixpkgs.vim \
    nixpkgs.neovim \
    nixpkgs.zsh \
    nixpkgs.tmux \
    nixpkgs.gnupg \
    nixpkgs.tree \
    nixpkgs.curl \
    nixpkgs.wget \
    nixpkgs.cacert \
    nixpkgs.nodejs \
    nixpkgs.gcc \
    nixpkgs.gnumake \
    nixpkgs.which

# ---
# Set up certificate environment for SSL
# ---
ENV SSL_CERT_FILE=/nix/store/$(ls /nix/store | grep -m1 "nss-cacert.*")/etc/ssl/certs/ca-bundle.crt
ENV NIX_SSL_CERT_FILE=$SSL_CERT_FILE

# ---
# Configure timezone
# ---
RUN ln -sf /nix/store/$(ls /nix/store | grep -m1 "tzdata.*")/share/zoneinfo/$TZ /etc/localtime

# ---
# Setup ZSH
#
# References:
#   [1] https://github.com/deluan/zsh-in-docker/blob/master/Dockerfile
# ---
COPY files/.zshrc files/.tmux.conf $HOME/

# Set zsh as default shell
ENV SHELL=/nix/var/nix/profiles/default/bin/zsh
SHELL ["/nix/var/nix/profiles/default/bin/zsh", "-c"]

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)" "" --unattended || true

RUN git clone --depth 1 https://github.com/romkatv/powerlevel10k $HOME/.oh-my-zsh/custom/themes/powerlevel10k || true

RUN git clone https://github.com/tmux-plugins/tpm $HOME/.tmux/plugins/tpm && \
    $HOME/.tmux/plugins/tpm/bin/install_plugins || true

# ---
# Install Python dependencies via Poetry
# ---
COPY pyproject.toml poetry.lock /usr/local/

RUN poetry config virtualenvs.create false && \
    cd /usr/local && \
    poetry install --no-interaction --no-ansi --no-root || true

ENV PATH="${PATH}:$HOME/.local/bin"

# ---
# Install Ruby Gems
# ---
RUN bundle config --global frozen 1

# Prepare to install ruby packages into container
COPY Gemfile Gemfile.lock minimal-mistakes-jekyll.gemspec $HOME/gems/

RUN cd $HOME/gems && bundle install

# ---
# Expose Jekyll port
# ---
EXPOSE 4000

# ---
# Default command
# ---
CMD ["jekyll", "serve", "--host", "0.0.0.0"]

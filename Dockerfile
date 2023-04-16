# ---
# Build arguments
# ---
ARG DOCKER_PARENT_IMAGE=ruby:2.5
FROM $DOCKER_PARENT_IMAGE

# NB: Arguments should come after FROM otherwise they're deleted
ARG BUILD_DATE
ARG PROJECT_NAME
ARG PYTHON_VERSION

# Silence debconf
ARG DEBIAN_FRONTEND=noninteractive

# ---
# Enviroment variables
# ---
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8
ENV TZ Australia/Sydney
ENV SHELL=/bin/bash
ENV HOME=/home/$PROJECT_NAME
ENV PYTHON_VERSION=$PYTHON_VERSION
# ---
# Set container time zone, maintainer and define home and workdir
# ---
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

LABEL org.label-schema.build-date=$BUILD_DATE \
    maintainer="Humberto STEIN SHIROMOTO <h.stein.shiromoto@gmail.com>"

RUN mkdir -p $HOME && mkdir -p $HOME/gems
WORKDIR $HOME

# ---
# Install Debian Packages
#
# References:
#   [1] https://unix.stackexchange.com/questions/336392/e-unable-to-locate-package-vim-on-debian-jessie-simplified-docker-container
# ---
RUN apt-get update && apt-get install apt-file -y && apt-file update && apt-get install -y git-flow vim zsh tmux

# ---
# Setup ZSH [1]
# 
# References
#   [1] https://github.com/deluan/zsh-in-docker/blob/master/Dockerfile
# ---
COPY bin/oh-my-zosh-install.sh /usr/local/
RUN /usr/local/oh-my-zosh-install.sh \
    -t https://github.com/denysdovhan/spaceship-prompt \
    -a 'SPACESHIP_PROMPT_ADD_NEWLINE="false"' \
    -a 'SPACESHIP_PROMPT_SEPARATE_LINE="false"' \
    -p git \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions \
    -p https://github.com/zsh-users/zsh-history-substring-search \
    -p https://github.com/zsh-users/zsh-syntax-highlighting \
    -p 'history-substring-search' \
    -a 'bindkey "\$terminfo[kcuu1]" history-substring-search-up' \
    -a 'bindkey "\$terminfo[kcud1]" history-substring-search-down'

# ---
# Install pyenv
#
# References:
#   [1] https://stackoverflow.com/questions/65768775/how-do-i-integrate-pyenv-poetry-and-docker
# ---
RUN git clone --depth=1 https://github.com/pyenv/pyenv.git $HOME/.pyenv
ENV PYENV_ROOT="${HOME}/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"

# ---
# Install Python and set the correct version
# ---
RUN pyenv install $PYTHON_VERSION && pyenv global $PYTHON_VERSION

# ---
# Install poetry
# ---
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="${PATH}:$HOME/.poetry/bin"
ENV PATH="${PATH}:$HOME/.local/bin"

COPY pyproject.toml poetry.lock /usr/local/

RUN poetry config virtualenvs.create false \
    && cd /usr/local \
    && poetry install --no-interaction --no-ansi

ENV PATH="${PATH}:$HOME/.local/bin"
# Need for Pytest
ENV PATH="${PATH}:${PYENV_ROOT}/versions/$PYTHON_VERSION/bin"

# ---
# Install Gems
# ---
RUN bundle config --global frozen 1

# prepare to install ruby packages into container
COPY Gemfile Gemfile.lock minimal-mistakes-jekyll.gemspec $HOME/gems/

RUN cd $HOME/gems && bundle install

EXPOSE 4000

CMD ["jekyll", "serve"]
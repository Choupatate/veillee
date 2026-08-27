FROM python:3.12-slim

# The release tag, so a family can say which version they are running when
# something goes wrong. `dev` for anyone building this themselves — which
# is honest: an image built from a working tree is not a release.
ARG VERSION=dev
ENV STORYBOOK_VERSION=$VERSION

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home --shell /usr/sbin/nologin storybook \
    && mkdir -p /data/stories \
    && chown -R storybook:storybook /app /data/stories

ENV STORYBOOK_STORIES_DIR=/data/stories
ENV PORT=5011
VOLUME ["/data/stories"]
EXPOSE 5011

USER storybook

CMD ["python", "serve.py"]

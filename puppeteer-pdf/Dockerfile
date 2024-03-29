# Enforce the platform to AMD64 to prevent unsupported ARM64 images that generated on Macbook M1 chips
FROM --platform=linux/amd64 node:10.15

RUN apt-get update && apt-get install -y wget --no-install-recommends \
  && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
  && apt-get update \
  && apt-get install -y google-chrome-unstable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst ttf-freefont libxtst6 libxss1 \
  --no-install-recommends \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get purge --auto-remove -y curl \
  && rm -rf /src/*.deb

ADD https://github.com/Yelp/dumb-init/releases/download/v1.2.0/dumb-init_1.2.0_amd64 /usr/local/bin/dumb-init
RUN chmod +x /usr/local/bin/dumb-init

WORKDIR /app
COPY . .

RUN npm install
RUN npm install puppeteer
EXPOSE 3000

ENTRYPOINT ["dumb-init", "--"]
CMD npm run start

FROM node:14

WORKDIR /app

COPY package*.json ./

RUN npm install
RUN npm install http-proxy-middleware --save

COPY . .

EXPOSE 8888

CMD ["npm", "start"]
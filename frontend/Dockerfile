FROM node:18

WORKDIR /app

COPY package*.json ./

RUN npm install
RUN npm install jquery

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

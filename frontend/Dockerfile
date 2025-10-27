FROM node:18

WORKDIR /app

COPY package*.json ./

RUN npm install
RUN npm install jquery

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]


# FROM node:18

# WORKDIR /app

# COPY package*.json ./

# RUN npm install

# COPY . .

# RUN npm run build

# RUN npm install -g serve

# EXPOSE 80

# CMD ["serve", "dist", "-s", "-l", "80"] 
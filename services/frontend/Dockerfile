FROM node:20-alpine

WORKDIR /app

COPY services/frontend/package.json /app/package.json
RUN npm install

COPY services/frontend /app

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]

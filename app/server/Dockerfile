# Install dependencies only when needed
FROM node:18-alpine AS deps
WORKDIR /app
COPY app/package.json yarn.lock* package-lock.json* ./
RUN npm install

# Production image, copy all the files and run the server
FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production

COPY --from=deps /app/node_modules ./node_modules
COPY app/ .

EXPOSE 3001

CMD ["npm", "start"]

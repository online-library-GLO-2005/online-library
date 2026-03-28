# === Frontend dockerfile ====

# Uses node version 22 as our base image
FROM node:22

# Goes to the app directory (this container will have app folder)
WORKDIR /app

# Copy package.json and package-lock.json and puts it in the cache of the container
COPY package*.json ./

# Install app dependencies (like npm install)
RUN npm ci

# Copy code into the container
COPY . .

# Expose the port (React's default port) 
EXPOSE 3000

# Run the app
CMD ["npm", "run", "dev"]


# ===== Once frontend is completed use this code: =====

# # Build step
# FROM node:22 AS build

# WORKDIR /app

# COPY package*.json ./
# RUN npm ci

# COPY . .
# RUN npm run build

# # Serve with nginx
# FROM nginx:alpine

# COPY --from=build /app/build /usr/share/nginx/html

# EXPOSE 80

# CMD ["nginx", "-g", "daemon off;"]
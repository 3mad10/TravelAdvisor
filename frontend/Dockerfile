# Use a Node.js base image
FROM node:20 as build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY travel-advisor/package*.json ./

# Install dependencies
RUN npm install

# Copy all the project files
COPY travel-advisor/ .

ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# Build the app
RUN npm run build

# Use a lightweight server image to serve the built app
FROM nginx:alpine

# Copy the built files from the previous stage to the Nginx web directory
COPY --from=build /app/dist /usr/share/nginx/html

# Expose the port Nginx is running on
EXPOSE 8080

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
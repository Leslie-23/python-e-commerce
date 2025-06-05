// require("dotenv").config();
// const express = require("express");
// const cors = require("cors");
// const morgan = require("morgan");
// const cookieParser = require("cookie-parser");
// const authRoutes = require("./routes/Auth");
// const productRoutes = require("./routes/Product");
// const orderRoutes = require("./routes/Order");
// const cartRoutes = require("./routes/Cart");
// const brandRoutes = require("./routes/Brand");
// const categoryRoutes = require("./routes/Category");
// const userRoutes = require("./routes/User");
// const addressRoutes = require("./routes/Address");
// const reviewRoutes = require("./routes/Review");
// const wishlistRoutes = require("./routes/Wishlist");
// const { connectToDB } = require("./database/db");

// // server init
// const server = express();

// // database connection
// connectToDB();

// // middlewares
// server.use(
//   cors({
//     origin: [process.env.ORIGIN_1, process.env.ORIGIN_2],
//     credentials: true,
//     exposedHeaders: ["X-Total-Count"],
//     methods: ["GET", "POST", "PATCH", "DELETE"],
//   })
// );
// server.use(express.json());
// server.use(cookieParser());
// server.use(morgan("tiny"));

// // routeMiddleware
// server.use("/auth", authRoutes);
// server.use("/users", userRoutes);
// server.use("/products", productRoutes);
// server.use("/orders", orderRoutes);
// server.use("/cart", cartRoutes);
// server.use("/brands", brandRoutes);
// server.use("/categories", categoryRoutes);
// server.use("/address", addressRoutes);
// server.use("/reviews", reviewRoutes);
// server.use("/wishlist", wishlistRoutes);

// server.get("/", (req, res) => {
//   res.status(200).json({ message: "running" });
// });

// const PORT = process.env.PORT || 8000;
// server.listen(PORT, () => {
//   console.log(`server [STARTED] ~ port: ${PORT}`);
// });

// require("dotenv").config();
// const express = require("express");
// const cors = require("cors");
// const morgan = require("morgan");
// const cookieParser = require("cookie-parser");
// const authRoutes = require("./routes/Auth");
// const productRoutes = require("./routes/Product");
// const orderRoutes = require("./routes/Order");
// const cartRoutes = require("./routes/Cart");
// const brandRoutes = require("./routes/Brand");
// const categoryRoutes = require("./routes/Category");
// const userRoutes = require("./routes/User");
// const addressRoutes = require("./routes/Address");
// const reviewRoutes = require("./routes/Review");
// const wishlistRoutes = require("./routes/Wishlist");
// const { connectToDB } = require("./database/db");

// // server init
// const server = express();

// // database connection
// connectToDB();

// // CORS configuration
// server.use(
//   cors({
//     origin: [process.env.ORIGIN_1, process.env.ORIGIN_2, process.env.ORIGIN_3],
//     credentials: true,
//     exposedHeaders: ["X-Total-Count"],
//     methods: ["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
//     allowedHeaders: ["Content-Type", "Authorization"],
//   })
// );

// // middlewares
// server.use(express.json());
// server.use(cookieParser());
// server.use(morgan("tiny"));

// // routeMiddleware
// server.use("/auth", authRoutes);
// server.use("/users", userRoutes);
// server.use("/products", productRoutes);
// server.use("/orders", orderRoutes);
// server.use("/cart", cartRoutes);
// server.use("/brands", brandRoutes);
// server.use("/categories", categoryRoutes);
// server.use("/address", addressRoutes);
// server.use("/reviews", reviewRoutes);
// server.use("/wishlist", wishlistRoutes);

// server.get("/", (req, res) => {
//   res.status(200).json({ message: "running" });
// });

// // Test OPTIONS request handling
// server.options(
//   "*",
//   cors({
//     origin: [process.env.ORIGIN_1, process.env.ORIGIN_2, process.env.ORIGIN_3],
//     credentials: true,
//     methods: ["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
//     allowedHeaders: ["Content-Type", "Authorization"],
//   })
// );

// server.options("*", (req, res) => {
//   res.setHeader(
//     "Access-Control-Allow-Origin",
//     "https://paltech-e-commerce.netlify.app"
//   );
//   res.setHeader(
//     "Access-Control-Allow-Methods",
//     "GET, POST, PATCH, DELETE, OPTIONS"
//   );
//   res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
//   res.setHeader("Access-Control-Allow-Credentials", "true");
//   res.sendStatus(204); // No Content
// });

// const PORT = process.env.PORT || 8000;
// server.listen(PORT, () => {
//   console.log(`server [STARTED] ~ port: ${PORT}`);
// });

// // ------------------------------------------------------>
// require("dotenv").config();
// const express = require("express");
// const cors = require("cors");
// const morgan = require("morgan");
// const cookieParser = require("cookie-parser");
// const authRoutes = require("./routes/Auth");
// const productRoutes = require("./routes/Product");
// const orderRoutes = require("./routes/Order");
// const cartRoutes = require("./routes/Cart");
// const brandRoutes = require("./routes/Brand");
// const categoryRoutes = require("./routes/Category");
// const userRoutes = require("./routes/User");
// const addressRoutes = require("./routes/Address");
// const reviewRoutes = require("./routes/Review");
// const wishlistRoutes = require("./routes/Wishlist");
// const { connectToDB } = require("./database/db");

// // server init
// const server = express();

// // database connection
// connectToDB();

// // CORS configuration
// server.use(
//   cors({
//     origin: [
//       process.env.ORIGIN_1,
//       process.env.ORIGIN_2,
//       process.env.ORIGIN_3,
//       process.env.ORIGIN_4,
//     ],
//     credentials: true,
//     exposedHeaders: ["X-Total-Count"],
//     methods: ["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
//     allowedHeaders: ["Content-Type", "Authorization", "application/json"],
//   })
// );

// // middlewares
// server.use(express.json());
// server.use(cookieParser());
// server.use(morgan("tiny"));

// // routeMiddleware
// server.use("/auth", authRoutes);
// server.use("/users", userRoutes);
// server.use("/products", productRoutes);
// server.use("/orders", orderRoutes);
// server.use("/cart", cartRoutes);
// server.use("/brands", brandRoutes);
// server.use("/categories", categoryRoutes);
// server.use("/address", addressRoutes);
// server.use("/reviews", reviewRoutes);
// server.use("/wishlist", wishlistRoutes);

// // Base route
// server.get("/", (req, res) => {
//   res.status(200).json({ message: "running" });
// });

// const allowedOrigins = [
//   process.env.ORIGIN_1,
//   process.env.ORIGIN_2,
//   process.env.ORIGIN_3,
//   process.env.ORIGIN_4,
// ];

// // Unified OPTIONS request handling
// server.options("*", (req, res) => {
//   // res.setHeader("Access-Control-Allow-Origin", "http://localhost:3000");
//   const origin = req.headers.origin;
//   // Set Access-Control-Allow-Origin to the origin of the request if it's in the allowedOrigins list
//   if (allowedOrigins.includes(origin)) {
//     res.setHeader("Access-Control-Allow-Origin", origin);
//   } //else {
//   //   res.setHeader("Access-Control-Allow-Origin", ""); // Or a default fallback origin if needed
//   // }

//   res.setHeader(
//     "Access-Control-Allow-Methods",
//     "GET, POST, PATCH, DELETE, OPTIONS"
//   );
//   res.setHeader(
//     "Access-Control-Allow-Headers",
//     "Content-Type, Authorization, application/json"
//   );
//   res.setHeader("Access-Control-Allow-Credentials", "true");
//   res.setHeader("Access-Control-Expose-Headers", "X-Total-Count");
//   res.sendStatus(204); // No Content
//   console.log(`REQUEST ORIGIN: ${origin}`);
// });

// const PORT = process.env.PORT || 8000;
// server.listen(PORT, () => {
//   console.log(`server [STARTED] ~ port: ${PORT}`);
// });

require("dotenv").config();
const express = require("express");
const cors = require("cors");
const morgan = require("morgan");
const cookieParser = require("cookie-parser");
const authRoutes = require("./routes/Auth");
const productRoutes = require("./routes/Product");
const orderRoutes = require("./routes/Order");
const cartRoutes = require("./routes/Cart");
const brandRoutes = require("./routes/Brand");
const categoryRoutes = require("./routes/Category");
const userRoutes = require("./routes/User");
const addressRoutes = require("./routes/Address");
const reviewRoutes = require("./routes/Review");
const wishlistRoutes = require("./routes/Wishlist");
const { connectToDB } = require("./database/db");

// server init
const server = express();

// database connection
connectToDB();

// middlewares
server.use(
  cors({
    origin: [
      "http://localhost:3000",
      "http://localhost:3001",
      "https://paltech-e-commerce.netlify.app",
    ],
    credentials: true,
    exposedHeaders: ["X-Total-Count"],
    methods: ["GET", "POST", "PATCH", "DELETE"],
  })
);
server.use(express.json());
server.use(cookieParser());
server.use(morgan("tiny"));

// routeMiddleware
server.use("/auth", authRoutes);
server.use("/users", userRoutes);
server.use("/products", productRoutes);
server.use("/orders", orderRoutes);
server.use("/cart", cartRoutes);
server.use("/brands", brandRoutes);
server.use("/categories", categoryRoutes);
server.use("/address", addressRoutes);
server.use("/reviews", reviewRoutes);
server.use("/wishlist", wishlistRoutes);

server.get("/", (req, res) => {
  res.status(200).json({ message: "running" });
});

server.listen(8000, () => {
  console.log("server [STARTED] ~ http://localhost:8000");
});

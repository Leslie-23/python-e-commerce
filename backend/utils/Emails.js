// const nodemailer = require("nodemailer");

// const transporter = nodemailer.createTransport({
//   service: "gmail",
//   auth: {
//     user: "leslieajayi27@gmail.com",
//     pass: "STARBOYLESLIE",
//   },
// });

// exports.sendMail = async (receiverEmail, subject, body) => {
//   await transporter.sendMail({
//     from: process.env.EMAIL,
//     to: receiverEmail,
//     subject: subject,
//     html: body,
//   });
// // };
// require("dotenv").config();
// const nodemailer = require("nodemailer");

// // Debugging: Check environment variables
// console.log("EMAIL:", process.env.EMAIL);
// console.log("EMAIL_PASSWORD:", process.env.PASSWORD);

// var transporter = nodemailer.createTransport({
//   host: "smtp.gmail.com",
//   port: 587,
//   auth: {
//     user: process.env.EMAIL,
//     pass: process.env.PASSWORD,
//   },
// });

// exports.sendMail = async (receiverEmail, subject, body) => {
//   try {
//     await transporter.sendMail({
//       from: process.env.EMAIL,
//       to: receiverEmail,
//       subject: subject,
//       html: body,
//     });
//     console.log(`${receiverEmail}`), console.log("Email sent successfully");
//   } catch (error) {
//     console.error("Error sending email:", error);
//   }
// };

// require("dotenv").config();
// const nodemailer = require("nodemailer");

// // Debugging: Check environment variables
// console.log("EMAIL:", process.env.EMAIL);
// console.log("EMAIL_PASSWORD:", process.env.PASSWORD);

// const transporter = nodemailer.createTransport({
//   service: "gmail",
//   port: 587,
//   secure: false, // Use TLS
//   auth: {
//     user: process.env.EMAIL,
//     pass: process.env.PASSWORD,
//   },
//   tls: {
//     rejectUnauthorized: false, // Optional: for self-signed certificates
//   },
// });

// exports.sendMail = async (receiverEmail, subject, body) => {
//   try {
//     await transporter.sendMail({
//       from: process.env.EMAIL,
//       to: receiverEmail,
//       subject: subject,
//       html: body,
//     });
//     console.log(`Email sent successfully to ${receiverEmail}`);
//   } catch (error) {
//     console.error("Error sending email:", error);
//   }
// };

// ----------------------------->
require("dotenv").config();
const nodemailer = require("nodemailer");

// Debugging: Check environment variables
console.log("EMAIL:", process.env.EMAIL);
console.log("EMAIL_PASSWORD:", process.env.PASSWORD);

const transporter = nodemailer.createTransport({
  service: "gmail", // Ensure you're using Gmail SMTP here
  secure: false, // Use TLS for secure connection
  auth: {
    // type: "login",
    user: process.env.EMAIL, // Your email
    pass: process.env.PASSWORD, // App Password if 2FA is on
  },
  // logger: "true",
  // debug: "true",
  // Optional: set to true if your production environment has stricter SSL policies
  tls: {
    rejectUnauthorized: false,
  },
});

exports.sendMail = async (receiverEmail, subject, body) => {
  try {
    await transporter.sendMail({
      from: process.env.EMAIL,
      to: receiverEmail,
      subject: subject,
      html: body,
    });
    console.log(`Email sent successfully to ${receiverEmail}`);
  } catch (error) {
    console.error("Error sending email:", error.message, error.stack);
  }
};

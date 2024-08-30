"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var prisma_lib_1 = require("prisma-client-lib");
var typeDefs = require("./prisma-schema").typeDefs;

var models = [
  {
    name: "Bill",
    embedded: false
  },
  {
    name: "Comment",
    embedded: false
  },
  {
    name: "Feed",
    embedded: false
  },
  {
    name: "Notification",
    embedded: false
  },
  {
    name: "Permission",
    embedded: false
  },
  {
    name: "Politician",
    embedded: false
  },
  {
    name: "Subscription",
    embedded: false
  },
  {
    name: "Topic",
    embedded: false
  },
  {
    name: "User",
    embedded: false
  }
];
exports.Prisma = prisma_lib_1.makePrismaClientClass({
  typeDefs,
  models,
  endpoint: `${process.env["PRISMA_ENDPOINT"]}`,
  secret: `${process.env["PRISMA_SECRET"]}`
});
exports.prisma = new exports.Prisma();

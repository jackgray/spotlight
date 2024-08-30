module.exports = {
        typeDefs: /* GraphQL */ `type AggregateBill {
  count: Int!
}

type AggregateComment {
  count: Int!
}

type AggregateFeed {
  count: Int!
}

type AggregateNotification {
  count: Int!
}

type AggregatePolitician {
  count: Int!
}

type AggregateSubscription {
  count: Int!
}

type AggregateTopic {
  count: Int!
}

type AggregateUser {
  count: Int!
}

type BatchPayload {
  count: Long!
}

type Bill {
  id: ID!
  code: String
  title: String
  summary: String
  congressNumber: String
  chamber: String
  committees: String
  link: String
  sponsor: String
  coSponsors(where: PoliticianWhereInput, orderBy: PoliticianOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Politician!]
  actions: [String!]!
  followers(where: UserWhereInput, orderBy: UserOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [User!]
  upvotes(where: UserWhereInput, orderBy: UserOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [User!]
  downvotes(where: UserWhereInput, orderBy: UserOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [User!]
  comments(where: CommentWhereInput, orderBy: CommentOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Comment!]
}

type BillConnection {
  pageInfo: PageInfo!
  edges: [BillEdge]!
  aggregate: AggregateBill!
}

input BillCreateactionsInput {
  set: [String!]
}

input BillCreateInput {
  code: String
  title: String
  summary: String
  congressNumber: String
  chamber: String
  committees: String
  link: String
  sponsor: String
  coSponsors: PoliticianCreateManyWithoutCoBillsInput
  actions: BillCreateactionsInput
  followers: UserCreateManyWithoutMyBillsInput
  upvotes: UserCreateManyWithoutUpvotedBillsInput
  downvotes: UserCreateManyWithoutDownvotedBillsInput
  comments: CommentCreateManyWithoutBillInput
}

input BillCreateManyInput {
  create: [BillCreateInput!]
  connect: [BillWhereUniqueInput!]
}

input BillCreateManyWithoutCoSponsorsInput {
  create: [BillCreateWithoutCoSponsorsInput!]
  connect: [BillWhereUniqueInput!]
}

input BillCreateManyWithoutDownvotesInput {
  create: [BillCreateWithoutDownvotesInput!]
  connect: [BillWhereUniqueInput!]
}

input BillCreateManyWithoutFollowersInput {
  create: [BillCreateWithoutFollowersInput!]
  connect: [BillWhereUniqueInput!]
}

input BillCreateManyWithoutUpvotesInput {
  create: [BillCreateWithoutUpvotesInput!]
  connect: [BillWhereUniqueInput!]
}

input BillCreateOneInput {
  create: BillCreateInput
  connect: BillWhereUniqueInput
}

input BillCreateOneWithoutCommentsInput {
  create: BillCreateWithoutCommentsInput
  connect: BillWhereUniqueInput
}

input BillCreateWithoutCommentsInput {
  code: String
  title: String
  summary: String
  congressNumber: String
  chamber: String
  committees: String
  link: String
  sponsor: String
  coSponsors: PoliticianCreateManyWithoutCoBillsInput
  actions: BillCreateactionsInput
  followers: UserCreateManyWithoutMyBillsInput
  upvotes: UserCreateManyWithoutUpvotedBillsInput
  downvotes: UserCreateManyWithoutDownvotedBillsInput
}

input BillCreateWithoutCoSponsorsInput {
  code: String
  title: String
  summary: String
  congressNumber: String
  chamber: String
  committees: String
  link: String
  sponsor: String
  actions: BillCreateactionsInput
  followers: UserCreateManyWithoutMyBillsInput
  upvotes: UserCreateManyWithoutUpvotedBillsInput
  downvotes: UserCreateManyWithoutDownvotedBillsInput
  comments: CommentCreateManyWithoutBillInput
}

input BillCreateWithoutDownvotesInput {
  code: String
  title: String
  summary: String
  congressNumber: String
  chamber: String
  committees: String
  link: String
  sponsor: String
  coSponsors: PoliticianCreateManyWithoutCoBillsInput
  actions: BillCreateactionsInput
  followers: UserCreateManyWithoutMyBillsInput
  upvotes: UserCreateManyWithoutUpvotedBillsInput
  comments: CommentCreateManyWithoutBillInput
}

input BillCreateWithoutFollowersInput {
  code: String
  title: String
  summary: String
  congressNumber: String
  chamber: String
  committees: String
  link: String
  sponsor: String
  coSponsors: PoliticianCreateManyWithoutCoBillsInput
  actions: BillCreateactionsInput
  upvotes: UserCreateManyWithoutUpvotedBillsInput
  downvotes: UserCreateManyWithoutDownvotedBillsInput
  comments: CommentCreateManyWithoutBillInput
}

input BillCreateWithoutUpvotesInput {
  code: String
  title: String
  summary: String
  congressNumber: String
  chamber: String
  committees: String
  link: String
  sponsor: String
  coSponsors: PoliticianCreateManyWithoutCoBillsInput
  actions: BillCreateactionsInput
  followers: UserCreateManyWithoutMyBillsInput
  downvotes: UserCreateManyWithoutDownvotedBillsInput
  comments: CommentCreateManyWithoutBillInput
}

type BillEdge {
  node: Bill!
  cursor: String!
}

enum BillOrderByInput {
  id_ASC
  id_DESC
  code_ASC
  code_DESC
  title_ASC
  title_DESC
  summary_ASC
  summary_DESC
  congressNumber_ASC
  congressNumber_DESC
  chamber_ASC
  chamber_DESC
  committees_ASC
  committees_DESC
  link_ASC
  link_DESC
  sponsor_ASC
  sponsor_DESC
  createdAt_ASC
  createdAt_DESC
  updatedAt_ASC
  updatedAt_DESC
}

input BillScalarWhereInput {
  id: ID
  id_not: ID
  id_in: [ID!]
  id_not_in: [ID!]
  id_lt: ID
  id_lte: ID
  id_gt: ID
  id_gte: ID
  id_contains: ID
  id_not_contains: ID
  id_starts_with: ID
  id_not_starts_with: ID
  id_ends_with: ID
  id_not_ends_with: ID
  code: String
  code_not: String
  code_in: [String!]
  code_not_in: [String!]
  code_lt: String
  code_lte: String
  code_gt: String
  code_gte: String
  code_contains: String
  code_not_contains: String
  code_starts_with: String
  code_not_starts_with: String
  code_ends_with: String
  code_not_ends_with: String
  title: String
  title_not: String
  title_in: [String!]
  title_not_in: [String!]
  title_lt: String
  title_lte: String
  title_gt: String
  title_gte: String
  title_contains: String
  title_not_contains: String
  title_starts_with: String
  title_not_starts_with: String
  title_ends_with: String
  title_not_ends_with: String
  summary: String
  summary_not: String
  summary_in: [String!]
  summary_not_in: [String!]
  summary_lt: String
  summary_lte: String
  summary_gt: String
  summary_gte: String
  summary_contains: String
  summary_not_contains: String
  summary_starts_with: String
  summary_not_starts_with: String
  summary_ends_with: String
  summary_not_ends_with: String
  congressNumber: String
  congressNumber_not: String
  congressNumber_in: [String!]
  congressNumber_not_in: [String!]
  congressNumber_lt: String
  congressNumber_lte: String
  congressNumber_gt: String
  congressNumber_gte: String
  congressNumber_contains: String
  congressNumber_not_contains: String
  congressNumber_starts_with: String
  congressNumber_not_starts_with: String
  congressNumber_ends_with: String
  congressNumber_not_ends_with: String
  chamber: String
  chamber_not: String
  chamber_in: [String!]
  chamber_not_in: [String!]
  chamber_lt: String
  chamber_lte: String
  chamber_gt: String
  chamber_gte: String
  chamber_contains: String
  chamber_not_contains: String
  chamber_starts_with: String
  chamber_not_starts_with: String
  chamber_ends_with: String
  chamber_not_ends_with: String
  committees: String
  committees_not: String
  committees_in: [String!]
  committees_not_in: [String!]
  committees_lt: String
  committees_lte: String
  committees_gt: String
  committees_gte: String
  committees_contains: String
  committees_not_contains: String
  committees_starts_with: String
  committees_not_starts_with: String
  committees_ends_with: String
  committees_not_ends_with: String
  link: String
  link_not: String
  link_in: [String!]
  link_not_in: [String!]
  link_lt: String
  link_lte: String
  link_gt: String
  link_gte: String
  link_contains: String
  link_not_contains: String
  link_starts_with: String
  link_not_starts_with: String
  link_ends_with: String
  link_not_ends_with: String
  sponsor: String
  sponsor_not: String
  sponsor_in: [String!]
  sponsor_not_in: [String!]
  sponsor_lt: String
  sponsor_lte: String
  sponsor_gt: String
  sponsor_gte: String
  sponsor_contains: String
  sponsor_not_contains: String
  sponsor_starts_with: String
  sponsor_not_starts_with: String
  sponsor_ends_with: String
  sponsor_not_ends_with: String
  AND: [BillScalarWhereInput!]
  OR: [BillScalarWhereInput!]
  NOT: [BillScalarWhereInput!]
}

input BillUpdateactionsInput {
  set: [String!]
}

input BillUpdateDataInput {
  code: String
  title: String
  summary: String
  congressNumber: String
  chamber: String
  committees: String
  link: String
  sponsor: String
  coSponsors: PoliticianUpdateManyWithoutCoBillsInput
  actions: BillUpdateactionsInput
  followers: UserUpdateManyWithoutMyBillsInput
  upvotes: UserUpdateManyWithoutUpvotedBillsInput
  downvotes: UserUpdateManyWithoutDownvotedBillsInput
  comments: CommentUpdateManyWithoutBillInput
}

input BillUpdateInput {
  code: String
  title: String
  summary: String
  congressNumber: String
  chamber: String
  committees: String
  link: String
  sponsor: String
  coSponsors: PoliticianUpdateManyWithoutCoBillsInput
  actions: BillUpdateactionsInput
  followers: UserUpdateManyWithoutMyBillsInput
  upvotes: UserUpdateManyWithoutUpvotedBillsInput
  downvotes: UserUpdateManyWithoutDownvotedBillsInput
  comments: CommentUpdateManyWithoutBillInput
}

input BillUpdateManyDataInput {
  code: String
  title: String
  summary: String
  congressNumber: String
  chamber: String
  committees: String
  link: String
  sponsor: String
  actions: BillUpdateactionsInput
}

input BillUpdateManyInput {
  create: [BillCreateInput!]
  update: [BillUpdateWithWhereUniqueNestedInput!]
  upsert: [BillUpsertWithWhereUniqueNestedInput!]
  delete: [BillWhereUniqueInput!]
  connect: [BillWhereUniqueInput!]
  disconnect: [BillWhereUniqueInput!]
  deleteMany: [BillScalarWhereInput!]
  updateMany: [BillUpdateManyWithWhereNestedInput!]
}

input BillUpdateManyMutationInput {
  code: String
  title: String
  summary: String
  congressNumber: String
  chamber: String
  committees: String
  link: String
  sponsor: String
  actions: BillUpdateactionsInput
}

input BillUpdateManyWithoutCoSponsorsInput {
  create: [BillCreateWithoutCoSponsorsInput!]
  delete: [BillWhereUniqueInput!]
  connect: [BillWhereUniqueInput!]
  disconnect: [BillWhereUniqueInput!]
  update: [BillUpdateWithWhereUniqueWithoutCoSponsorsInput!]
  upsert: [BillUpsertWithWhereUniqueWithoutCoSponsorsInput!]
  deleteMany: [BillScalarWhereInput!]
  updateMany: [BillUpdateManyWithWhereNestedInput!]
}

input BillUpdateManyWithoutDownvotesInput {
  create: [BillCreateWithoutDownvotesInput!]
  delete: [BillWhereUniqueInput!]
  connect: [BillWhereUniqueInput!]
  disconnect: [BillWhereUniqueInput!]
  update: [BillUpdateWithWhereUniqueWithoutDownvotesInput!]
  upsert: [BillUpsertWithWhereUniqueWithoutDownvotesInput!]
  deleteMany: [BillScalarWhereInput!]
  updateMany: [BillUpdateManyWithWhereNestedInput!]
}

input BillUpdateManyWithoutFollowersInput {
  create: [BillCreateWithoutFollowersInput!]
  delete: [BillWhereUniqueInput!]
  connect: [BillWhereUniqueInput!]
  disconnect: [BillWhereUniqueInput!]
  update: [BillUpdateWithWhereUniqueWithoutFollowersInput!]
  upsert: [BillUpsertWithWhereUniqueWithoutFollowersInput!]
  deleteMany: [BillScalarWhereInput!]
  updateMany: [BillUpdateManyWithWhereNestedInput!]
}

input BillUpdateManyWithoutUpvotesInput {
  create: [BillCreateWithoutUpvotesInput!]
  delete: [BillWhereUniqueInput!]
  connect: [BillWhereUniqueInput!]
  disconnect: [BillWhereUniqueInput!]
  update: [BillUpdateWithWhereUniqueWithoutUpvotesInput!]
  upsert: [BillUpsertWithWhereUniqueWithoutUpvotesInput!]
  deleteMany: [BillScalarWhereInput!]
  updateMany: [BillUpdateManyWithWhereNestedInput!]
}

input BillUpdateManyWithWhereNestedInput {
  where: BillScalarWhereInput!
  data: BillUpdateManyDataInput!
}

input BillUpdateOneWithoutCommentsInput {
  create: BillCreateWithoutCommentsInput
  update: BillUpdateWithoutCommentsDataInput
  upsert: BillUpsertWithoutCommentsInput
  delete: Boolean
  disconnect: Boolean
  connect: BillWhereUniqueInput
}

input BillUpdateWithoutCommentsDataInput {
  code: String
  title: String
  summary: String
  congressNumber: String
  chamber: String
  committees: String
  link: String
  sponsor: String
  coSponsors: PoliticianUpdateManyWithoutCoBillsInput
  actions: BillUpdateactionsInput
  followers: UserUpdateManyWithoutMyBillsInput
  upvotes: UserUpdateManyWithoutUpvotedBillsInput
  downvotes: UserUpdateManyWithoutDownvotedBillsInput
}

input BillUpdateWithoutCoSponsorsDataInput {
  code: String
  title: String
  summary: String
  congressNumber: String
  chamber: String
  committees: String
  link: String
  sponsor: String
  actions: BillUpdateactionsInput
  followers: UserUpdateManyWithoutMyBillsInput
  upvotes: UserUpdateManyWithoutUpvotedBillsInput
  downvotes: UserUpdateManyWithoutDownvotedBillsInput
  comments: CommentUpdateManyWithoutBillInput
}

input BillUpdateWithoutDownvotesDataInput {
  code: String
  title: String
  summary: String
  congressNumber: String
  chamber: String
  committees: String
  link: String
  sponsor: String
  coSponsors: PoliticianUpdateManyWithoutCoBillsInput
  actions: BillUpdateactionsInput
  followers: UserUpdateManyWithoutMyBillsInput
  upvotes: UserUpdateManyWithoutUpvotedBillsInput
  comments: CommentUpdateManyWithoutBillInput
}

input BillUpdateWithoutFollowersDataInput {
  code: String
  title: String
  summary: String
  congressNumber: String
  chamber: String
  committees: String
  link: String
  sponsor: String
  coSponsors: PoliticianUpdateManyWithoutCoBillsInput
  actions: BillUpdateactionsInput
  upvotes: UserUpdateManyWithoutUpvotedBillsInput
  downvotes: UserUpdateManyWithoutDownvotedBillsInput
  comments: CommentUpdateManyWithoutBillInput
}

input BillUpdateWithoutUpvotesDataInput {
  code: String
  title: String
  summary: String
  congressNumber: String
  chamber: String
  committees: String
  link: String
  sponsor: String
  coSponsors: PoliticianUpdateManyWithoutCoBillsInput
  actions: BillUpdateactionsInput
  followers: UserUpdateManyWithoutMyBillsInput
  downvotes: UserUpdateManyWithoutDownvotedBillsInput
  comments: CommentUpdateManyWithoutBillInput
}

input BillUpdateWithWhereUniqueNestedInput {
  where: BillWhereUniqueInput!
  data: BillUpdateDataInput!
}

input BillUpdateWithWhereUniqueWithoutCoSponsorsInput {
  where: BillWhereUniqueInput!
  data: BillUpdateWithoutCoSponsorsDataInput!
}

input BillUpdateWithWhereUniqueWithoutDownvotesInput {
  where: BillWhereUniqueInput!
  data: BillUpdateWithoutDownvotesDataInput!
}

input BillUpdateWithWhereUniqueWithoutFollowersInput {
  where: BillWhereUniqueInput!
  data: BillUpdateWithoutFollowersDataInput!
}

input BillUpdateWithWhereUniqueWithoutUpvotesInput {
  where: BillWhereUniqueInput!
  data: BillUpdateWithoutUpvotesDataInput!
}

input BillUpsertWithoutCommentsInput {
  update: BillUpdateWithoutCommentsDataInput!
  create: BillCreateWithoutCommentsInput!
}

input BillUpsertWithWhereUniqueNestedInput {
  where: BillWhereUniqueInput!
  update: BillUpdateDataInput!
  create: BillCreateInput!
}

input BillUpsertWithWhereUniqueWithoutCoSponsorsInput {
  where: BillWhereUniqueInput!
  update: BillUpdateWithoutCoSponsorsDataInput!
  create: BillCreateWithoutCoSponsorsInput!
}

input BillUpsertWithWhereUniqueWithoutDownvotesInput {
  where: BillWhereUniqueInput!
  update: BillUpdateWithoutDownvotesDataInput!
  create: BillCreateWithoutDownvotesInput!
}

input BillUpsertWithWhereUniqueWithoutFollowersInput {
  where: BillWhereUniqueInput!
  update: BillUpdateWithoutFollowersDataInput!
  create: BillCreateWithoutFollowersInput!
}

input BillUpsertWithWhereUniqueWithoutUpvotesInput {
  where: BillWhereUniqueInput!
  update: BillUpdateWithoutUpvotesDataInput!
  create: BillCreateWithoutUpvotesInput!
}

input BillWhereInput {
  id: ID
  id_not: ID
  id_in: [ID!]
  id_not_in: [ID!]
  id_lt: ID
  id_lte: ID
  id_gt: ID
  id_gte: ID
  id_contains: ID
  id_not_contains: ID
  id_starts_with: ID
  id_not_starts_with: ID
  id_ends_with: ID
  id_not_ends_with: ID
  code: String
  code_not: String
  code_in: [String!]
  code_not_in: [String!]
  code_lt: String
  code_lte: String
  code_gt: String
  code_gte: String
  code_contains: String
  code_not_contains: String
  code_starts_with: String
  code_not_starts_with: String
  code_ends_with: String
  code_not_ends_with: String
  title: String
  title_not: String
  title_in: [String!]
  title_not_in: [String!]
  title_lt: String
  title_lte: String
  title_gt: String
  title_gte: String
  title_contains: String
  title_not_contains: String
  title_starts_with: String
  title_not_starts_with: String
  title_ends_with: String
  title_not_ends_with: String
  summary: String
  summary_not: String
  summary_in: [String!]
  summary_not_in: [String!]
  summary_lt: String
  summary_lte: String
  summary_gt: String
  summary_gte: String
  summary_contains: String
  summary_not_contains: String
  summary_starts_with: String
  summary_not_starts_with: String
  summary_ends_with: String
  summary_not_ends_with: String
  congressNumber: String
  congressNumber_not: String
  congressNumber_in: [String!]
  congressNumber_not_in: [String!]
  congressNumber_lt: String
  congressNumber_lte: String
  congressNumber_gt: String
  congressNumber_gte: String
  congressNumber_contains: String
  congressNumber_not_contains: String
  congressNumber_starts_with: String
  congressNumber_not_starts_with: String
  congressNumber_ends_with: String
  congressNumber_not_ends_with: String
  chamber: String
  chamber_not: String
  chamber_in: [String!]
  chamber_not_in: [String!]
  chamber_lt: String
  chamber_lte: String
  chamber_gt: String
  chamber_gte: String
  chamber_contains: String
  chamber_not_contains: String
  chamber_starts_with: String
  chamber_not_starts_with: String
  chamber_ends_with: String
  chamber_not_ends_with: String
  committees: String
  committees_not: String
  committees_in: [String!]
  committees_not_in: [String!]
  committees_lt: String
  committees_lte: String
  committees_gt: String
  committees_gte: String
  committees_contains: String
  committees_not_contains: String
  committees_starts_with: String
  committees_not_starts_with: String
  committees_ends_with: String
  committees_not_ends_with: String
  link: String
  link_not: String
  link_in: [String!]
  link_not_in: [String!]
  link_lt: String
  link_lte: String
  link_gt: String
  link_gte: String
  link_contains: String
  link_not_contains: String
  link_starts_with: String
  link_not_starts_with: String
  link_ends_with: String
  link_not_ends_with: String
  sponsor: String
  sponsor_not: String
  sponsor_in: [String!]
  sponsor_not_in: [String!]
  sponsor_lt: String
  sponsor_lte: String
  sponsor_gt: String
  sponsor_gte: String
  sponsor_contains: String
  sponsor_not_contains: String
  sponsor_starts_with: String
  sponsor_not_starts_with: String
  sponsor_ends_with: String
  sponsor_not_ends_with: String
  coSponsors_every: PoliticianWhereInput
  coSponsors_some: PoliticianWhereInput
  coSponsors_none: PoliticianWhereInput
  followers_every: UserWhereInput
  followers_some: UserWhereInput
  followers_none: UserWhereInput
  upvotes_every: UserWhereInput
  upvotes_some: UserWhereInput
  upvotes_none: UserWhereInput
  downvotes_every: UserWhereInput
  downvotes_some: UserWhereInput
  downvotes_none: UserWhereInput
  comments_every: CommentWhereInput
  comments_some: CommentWhereInput
  comments_none: CommentWhereInput
  AND: [BillWhereInput!]
  OR: [BillWhereInput!]
  NOT: [BillWhereInput!]
}

input BillWhereUniqueInput {
  id: ID
}

type Comment {
  id: ID!
  content: String
  reply: String
  bill: Bill
  author: User
  politiciansMentioned(where: PoliticianWhereInput, orderBy: PoliticianOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Politician!]
  topic: Topic
}

type CommentConnection {
  pageInfo: PageInfo!
  edges: [CommentEdge]!
  aggregate: AggregateComment!
}

input CommentCreateInput {
  content: String
  reply: String
  bill: BillCreateOneWithoutCommentsInput
  author: UserCreateOneWithoutBillCommentsInput
  politiciansMentioned: PoliticianCreateManyWithoutMentionsInput
  topic: TopicCreateOneWithoutCommentsInput
}

input CommentCreateManyWithoutAuthorInput {
  create: [CommentCreateWithoutAuthorInput!]
  connect: [CommentWhereUniqueInput!]
}

input CommentCreateManyWithoutBillInput {
  create: [CommentCreateWithoutBillInput!]
  connect: [CommentWhereUniqueInput!]
}

input CommentCreateManyWithoutPoliticiansMentionedInput {
  create: [CommentCreateWithoutPoliticiansMentionedInput!]
  connect: [CommentWhereUniqueInput!]
}

input CommentCreateManyWithoutTopicInput {
  create: [CommentCreateWithoutTopicInput!]
  connect: [CommentWhereUniqueInput!]
}

input CommentCreateOneInput {
  create: CommentCreateInput
  connect: CommentWhereUniqueInput
}

input CommentCreateWithoutAuthorInput {
  content: String
  reply: String
  bill: BillCreateOneWithoutCommentsInput
  politiciansMentioned: PoliticianCreateManyWithoutMentionsInput
  topic: TopicCreateOneWithoutCommentsInput
}

input CommentCreateWithoutBillInput {
  content: String
  reply: String
  author: UserCreateOneWithoutBillCommentsInput
  politiciansMentioned: PoliticianCreateManyWithoutMentionsInput
  topic: TopicCreateOneWithoutCommentsInput
}

input CommentCreateWithoutPoliticiansMentionedInput {
  content: String
  reply: String
  bill: BillCreateOneWithoutCommentsInput
  author: UserCreateOneWithoutBillCommentsInput
  topic: TopicCreateOneWithoutCommentsInput
}

input CommentCreateWithoutTopicInput {
  content: String
  reply: String
  bill: BillCreateOneWithoutCommentsInput
  author: UserCreateOneWithoutBillCommentsInput
  politiciansMentioned: PoliticianCreateManyWithoutMentionsInput
}

type CommentEdge {
  node: Comment!
  cursor: String!
}

enum CommentOrderByInput {
  id_ASC
  id_DESC
  content_ASC
  content_DESC
  reply_ASC
  reply_DESC
  createdAt_ASC
  createdAt_DESC
  updatedAt_ASC
  updatedAt_DESC
}

input CommentScalarWhereInput {
  id: ID
  id_not: ID
  id_in: [ID!]
  id_not_in: [ID!]
  id_lt: ID
  id_lte: ID
  id_gt: ID
  id_gte: ID
  id_contains: ID
  id_not_contains: ID
  id_starts_with: ID
  id_not_starts_with: ID
  id_ends_with: ID
  id_not_ends_with: ID
  content: String
  content_not: String
  content_in: [String!]
  content_not_in: [String!]
  content_lt: String
  content_lte: String
  content_gt: String
  content_gte: String
  content_contains: String
  content_not_contains: String
  content_starts_with: String
  content_not_starts_with: String
  content_ends_with: String
  content_not_ends_with: String
  reply: String
  reply_not: String
  reply_in: [String!]
  reply_not_in: [String!]
  reply_lt: String
  reply_lte: String
  reply_gt: String
  reply_gte: String
  reply_contains: String
  reply_not_contains: String
  reply_starts_with: String
  reply_not_starts_with: String
  reply_ends_with: String
  reply_not_ends_with: String
  AND: [CommentScalarWhereInput!]
  OR: [CommentScalarWhereInput!]
  NOT: [CommentScalarWhereInput!]
}

input CommentUpdateInput {
  content: String
  reply: String
  bill: BillUpdateOneWithoutCommentsInput
  author: UserUpdateOneWithoutBillCommentsInput
  politiciansMentioned: PoliticianUpdateManyWithoutMentionsInput
  topic: TopicUpdateOneWithoutCommentsInput
}

input CommentUpdateManyDataInput {
  content: String
  reply: String
}

input CommentUpdateManyMutationInput {
  content: String
  reply: String
}

input CommentUpdateManyWithoutAuthorInput {
  create: [CommentCreateWithoutAuthorInput!]
  delete: [CommentWhereUniqueInput!]
  connect: [CommentWhereUniqueInput!]
  disconnect: [CommentWhereUniqueInput!]
  update: [CommentUpdateWithWhereUniqueWithoutAuthorInput!]
  upsert: [CommentUpsertWithWhereUniqueWithoutAuthorInput!]
  deleteMany: [CommentScalarWhereInput!]
  updateMany: [CommentUpdateManyWithWhereNestedInput!]
}

input CommentUpdateManyWithoutBillInput {
  create: [CommentCreateWithoutBillInput!]
  delete: [CommentWhereUniqueInput!]
  connect: [CommentWhereUniqueInput!]
  disconnect: [CommentWhereUniqueInput!]
  update: [CommentUpdateWithWhereUniqueWithoutBillInput!]
  upsert: [CommentUpsertWithWhereUniqueWithoutBillInput!]
  deleteMany: [CommentScalarWhereInput!]
  updateMany: [CommentUpdateManyWithWhereNestedInput!]
}

input CommentUpdateManyWithoutPoliticiansMentionedInput {
  create: [CommentCreateWithoutPoliticiansMentionedInput!]
  delete: [CommentWhereUniqueInput!]
  connect: [CommentWhereUniqueInput!]
  disconnect: [CommentWhereUniqueInput!]
  update: [CommentUpdateWithWhereUniqueWithoutPoliticiansMentionedInput!]
  upsert: [CommentUpsertWithWhereUniqueWithoutPoliticiansMentionedInput!]
  deleteMany: [CommentScalarWhereInput!]
  updateMany: [CommentUpdateManyWithWhereNestedInput!]
}

input CommentUpdateManyWithoutTopicInput {
  create: [CommentCreateWithoutTopicInput!]
  delete: [CommentWhereUniqueInput!]
  connect: [CommentWhereUniqueInput!]
  disconnect: [CommentWhereUniqueInput!]
  update: [CommentUpdateWithWhereUniqueWithoutTopicInput!]
  upsert: [CommentUpsertWithWhereUniqueWithoutTopicInput!]
  deleteMany: [CommentScalarWhereInput!]
  updateMany: [CommentUpdateManyWithWhereNestedInput!]
}

input CommentUpdateManyWithWhereNestedInput {
  where: CommentScalarWhereInput!
  data: CommentUpdateManyDataInput!
}

input CommentUpdateWithoutAuthorDataInput {
  content: String
  reply: String
  bill: BillUpdateOneWithoutCommentsInput
  politiciansMentioned: PoliticianUpdateManyWithoutMentionsInput
  topic: TopicUpdateOneWithoutCommentsInput
}

input CommentUpdateWithoutBillDataInput {
  content: String
  reply: String
  author: UserUpdateOneWithoutBillCommentsInput
  politiciansMentioned: PoliticianUpdateManyWithoutMentionsInput
  topic: TopicUpdateOneWithoutCommentsInput
}

input CommentUpdateWithoutPoliticiansMentionedDataInput {
  content: String
  reply: String
  bill: BillUpdateOneWithoutCommentsInput
  author: UserUpdateOneWithoutBillCommentsInput
  topic: TopicUpdateOneWithoutCommentsInput
}

input CommentUpdateWithoutTopicDataInput {
  content: String
  reply: String
  bill: BillUpdateOneWithoutCommentsInput
  author: UserUpdateOneWithoutBillCommentsInput
  politiciansMentioned: PoliticianUpdateManyWithoutMentionsInput
}

input CommentUpdateWithWhereUniqueWithoutAuthorInput {
  where: CommentWhereUniqueInput!
  data: CommentUpdateWithoutAuthorDataInput!
}

input CommentUpdateWithWhereUniqueWithoutBillInput {
  where: CommentWhereUniqueInput!
  data: CommentUpdateWithoutBillDataInput!
}

input CommentUpdateWithWhereUniqueWithoutPoliticiansMentionedInput {
  where: CommentWhereUniqueInput!
  data: CommentUpdateWithoutPoliticiansMentionedDataInput!
}

input CommentUpdateWithWhereUniqueWithoutTopicInput {
  where: CommentWhereUniqueInput!
  data: CommentUpdateWithoutTopicDataInput!
}

input CommentUpsertWithWhereUniqueWithoutAuthorInput {
  where: CommentWhereUniqueInput!
  update: CommentUpdateWithoutAuthorDataInput!
  create: CommentCreateWithoutAuthorInput!
}

input CommentUpsertWithWhereUniqueWithoutBillInput {
  where: CommentWhereUniqueInput!
  update: CommentUpdateWithoutBillDataInput!
  create: CommentCreateWithoutBillInput!
}

input CommentUpsertWithWhereUniqueWithoutPoliticiansMentionedInput {
  where: CommentWhereUniqueInput!
  update: CommentUpdateWithoutPoliticiansMentionedDataInput!
  create: CommentCreateWithoutPoliticiansMentionedInput!
}

input CommentUpsertWithWhereUniqueWithoutTopicInput {
  where: CommentWhereUniqueInput!
  update: CommentUpdateWithoutTopicDataInput!
  create: CommentCreateWithoutTopicInput!
}

input CommentWhereInput {
  id: ID
  id_not: ID
  id_in: [ID!]
  id_not_in: [ID!]
  id_lt: ID
  id_lte: ID
  id_gt: ID
  id_gte: ID
  id_contains: ID
  id_not_contains: ID
  id_starts_with: ID
  id_not_starts_with: ID
  id_ends_with: ID
  id_not_ends_with: ID
  content: String
  content_not: String
  content_in: [String!]
  content_not_in: [String!]
  content_lt: String
  content_lte: String
  content_gt: String
  content_gte: String
  content_contains: String
  content_not_contains: String
  content_starts_with: String
  content_not_starts_with: String
  content_ends_with: String
  content_not_ends_with: String
  reply: String
  reply_not: String
  reply_in: [String!]
  reply_not_in: [String!]
  reply_lt: String
  reply_lte: String
  reply_gt: String
  reply_gte: String
  reply_contains: String
  reply_not_contains: String
  reply_starts_with: String
  reply_not_starts_with: String
  reply_ends_with: String
  reply_not_ends_with: String
  bill: BillWhereInput
  author: UserWhereInput
  politiciansMentioned_every: PoliticianWhereInput
  politiciansMentioned_some: PoliticianWhereInput
  politiciansMentioned_none: PoliticianWhereInput
  topic: TopicWhereInput
  AND: [CommentWhereInput!]
  OR: [CommentWhereInput!]
  NOT: [CommentWhereInput!]
}

input CommentWhereUniqueInput {
  id: ID
}

scalar DateTime

type Feed {
  politicians(where: PoliticianWhereInput, orderBy: PoliticianOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Politician!]
  bills(where: BillWhereInput, orderBy: BillOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Bill!]
  count: Int!
}

type FeedConnection {
  pageInfo: PageInfo!
  edges: [FeedEdge]!
  aggregate: AggregateFeed!
}

input FeedCreateInput {
  politicians: PoliticianCreateManyInput
  bills: BillCreateManyInput
  count: Int!
}

type FeedEdge {
  node: Feed!
  cursor: String!
}

enum FeedOrderByInput {
  count_ASC
  count_DESC
  id_ASC
  id_DESC
  createdAt_ASC
  createdAt_DESC
  updatedAt_ASC
  updatedAt_DESC
}

input FeedUpdateManyMutationInput {
  count: Int
}

input FeedWhereInput {
  politicians_every: PoliticianWhereInput
  politicians_some: PoliticianWhereInput
  politicians_none: PoliticianWhereInput
  bills_every: BillWhereInput
  bills_some: BillWhereInput
  bills_none: BillWhereInput
  count: Int
  count_not: Int
  count_in: [Int!]
  count_not_in: [Int!]
  count_lt: Int
  count_lte: Int
  count_gt: Int
  count_gte: Int
  AND: [FeedWhereInput!]
  OR: [FeedWhereInput!]
  NOT: [FeedWhereInput!]
}

scalar Long

type Mutation {
  createBill(data: BillCreateInput!): Bill!
  updateBill(data: BillUpdateInput!, where: BillWhereUniqueInput!): Bill
  updateManyBills(data: BillUpdateManyMutationInput!, where: BillWhereInput): BatchPayload!
  upsertBill(where: BillWhereUniqueInput!, create: BillCreateInput!, update: BillUpdateInput!): Bill!
  deleteBill(where: BillWhereUniqueInput!): Bill
  deleteManyBills(where: BillWhereInput): BatchPayload!
  createComment(data: CommentCreateInput!): Comment!
  updateComment(data: CommentUpdateInput!, where: CommentWhereUniqueInput!): Comment
  updateManyComments(data: CommentUpdateManyMutationInput!, where: CommentWhereInput): BatchPayload!
  upsertComment(where: CommentWhereUniqueInput!, create: CommentCreateInput!, update: CommentUpdateInput!): Comment!
  deleteComment(where: CommentWhereUniqueInput!): Comment
  deleteManyComments(where: CommentWhereInput): BatchPayload!
  createFeed(data: FeedCreateInput!): Feed!
  updateManyFeeds(data: FeedUpdateManyMutationInput!, where: FeedWhereInput): BatchPayload!
  deleteManyFeeds(where: FeedWhereInput): BatchPayload!
  createNotification(data: NotificationCreateInput!): Notification!
  updateNotification(data: NotificationUpdateInput!, where: NotificationWhereUniqueInput!): Notification
  updateManyNotifications(data: NotificationUpdateManyMutationInput!, where: NotificationWhereInput): BatchPayload!
  upsertNotification(where: NotificationWhereUniqueInput!, create: NotificationCreateInput!, update: NotificationUpdateInput!): Notification!
  deleteNotification(where: NotificationWhereUniqueInput!): Notification
  deleteManyNotifications(where: NotificationWhereInput): BatchPayload!
  createPolitician(data: PoliticianCreateInput!): Politician!
  updatePolitician(data: PoliticianUpdateInput!, where: PoliticianWhereUniqueInput!): Politician
  updateManyPoliticians(data: PoliticianUpdateManyMutationInput!, where: PoliticianWhereInput): BatchPayload!
  upsertPolitician(where: PoliticianWhereUniqueInput!, create: PoliticianCreateInput!, update: PoliticianUpdateInput!): Politician!
  deletePolitician(where: PoliticianWhereUniqueInput!): Politician
  deleteManyPoliticians(where: PoliticianWhereInput): BatchPayload!
  createSubscription(data: SubscriptionCreateInput!): Subscription!
  deleteManySubscriptions(where: SubscriptionWhereInput): BatchPayload!
  createTopic(data: TopicCreateInput!): Topic!
  updateTopic(data: TopicUpdateInput!, where: TopicWhereUniqueInput!): Topic
  updateManyTopics(data: TopicUpdateManyMutationInput!, where: TopicWhereInput): BatchPayload!
  upsertTopic(where: TopicWhereUniqueInput!, create: TopicCreateInput!, update: TopicUpdateInput!): Topic!
  deleteTopic(where: TopicWhereUniqueInput!): Topic
  deleteManyTopics(where: TopicWhereInput): BatchPayload!
  createUser(data: UserCreateInput!): User!
  updateUser(data: UserUpdateInput!, where: UserWhereUniqueInput!): User
  updateManyUsers(data: UserUpdateManyMutationInput!, where: UserWhereInput): BatchPayload!
  upsertUser(where: UserWhereUniqueInput!, create: UserCreateInput!, update: UserUpdateInput!): User!
  deleteUser(where: UserWhereUniqueInput!): User
  deleteManyUsers(where: UserWhereInput): BatchPayload!
}

interface Node {
  id: ID!
}

type Notification {
  id: ID!
  label: String
  type: String
  user: User
}

type NotificationConnection {
  pageInfo: PageInfo!
  edges: [NotificationEdge]!
  aggregate: AggregateNotification!
}

input NotificationCreateInput {
  label: String
  type: String
  user: UserCreateOneWithoutNotificationsInput
}

input NotificationCreateManyWithoutUserInput {
  create: [NotificationCreateWithoutUserInput!]
  connect: [NotificationWhereUniqueInput!]
}

input NotificationCreateWithoutUserInput {
  label: String
  type: String
}

type NotificationEdge {
  node: Notification!
  cursor: String!
}

enum NotificationOrderByInput {
  id_ASC
  id_DESC
  label_ASC
  label_DESC
  type_ASC
  type_DESC
  createdAt_ASC
  createdAt_DESC
  updatedAt_ASC
  updatedAt_DESC
}

input NotificationScalarWhereInput {
  id: ID
  id_not: ID
  id_in: [ID!]
  id_not_in: [ID!]
  id_lt: ID
  id_lte: ID
  id_gt: ID
  id_gte: ID
  id_contains: ID
  id_not_contains: ID
  id_starts_with: ID
  id_not_starts_with: ID
  id_ends_with: ID
  id_not_ends_with: ID
  label: String
  label_not: String
  label_in: [String!]
  label_not_in: [String!]
  label_lt: String
  label_lte: String
  label_gt: String
  label_gte: String
  label_contains: String
  label_not_contains: String
  label_starts_with: String
  label_not_starts_with: String
  label_ends_with: String
  label_not_ends_with: String
  type: String
  type_not: String
  type_in: [String!]
  type_not_in: [String!]
  type_lt: String
  type_lte: String
  type_gt: String
  type_gte: String
  type_contains: String
  type_not_contains: String
  type_starts_with: String
  type_not_starts_with: String
  type_ends_with: String
  type_not_ends_with: String
  AND: [NotificationScalarWhereInput!]
  OR: [NotificationScalarWhereInput!]
  NOT: [NotificationScalarWhereInput!]
}

input NotificationUpdateInput {
  label: String
  type: String
  user: UserUpdateOneWithoutNotificationsInput
}

input NotificationUpdateManyDataInput {
  label: String
  type: String
}

input NotificationUpdateManyMutationInput {
  label: String
  type: String
}

input NotificationUpdateManyWithoutUserInput {
  create: [NotificationCreateWithoutUserInput!]
  delete: [NotificationWhereUniqueInput!]
  connect: [NotificationWhereUniqueInput!]
  disconnect: [NotificationWhereUniqueInput!]
  update: [NotificationUpdateWithWhereUniqueWithoutUserInput!]
  upsert: [NotificationUpsertWithWhereUniqueWithoutUserInput!]
  deleteMany: [NotificationScalarWhereInput!]
  updateMany: [NotificationUpdateManyWithWhereNestedInput!]
}

input NotificationUpdateManyWithWhereNestedInput {
  where: NotificationScalarWhereInput!
  data: NotificationUpdateManyDataInput!
}

input NotificationUpdateWithoutUserDataInput {
  label: String
  type: String
}

input NotificationUpdateWithWhereUniqueWithoutUserInput {
  where: NotificationWhereUniqueInput!
  data: NotificationUpdateWithoutUserDataInput!
}

input NotificationUpsertWithWhereUniqueWithoutUserInput {
  where: NotificationWhereUniqueInput!
  update: NotificationUpdateWithoutUserDataInput!
  create: NotificationCreateWithoutUserInput!
}

input NotificationWhereInput {
  id: ID
  id_not: ID
  id_in: [ID!]
  id_not_in: [ID!]
  id_lt: ID
  id_lte: ID
  id_gt: ID
  id_gte: ID
  id_contains: ID
  id_not_contains: ID
  id_starts_with: ID
  id_not_starts_with: ID
  id_ends_with: ID
  id_not_ends_with: ID
  label: String
  label_not: String
  label_in: [String!]
  label_not_in: [String!]
  label_lt: String
  label_lte: String
  label_gt: String
  label_gte: String
  label_contains: String
  label_not_contains: String
  label_starts_with: String
  label_not_starts_with: String
  label_ends_with: String
  label_not_ends_with: String
  type: String
  type_not: String
  type_in: [String!]
  type_not_in: [String!]
  type_lt: String
  type_lte: String
  type_gt: String
  type_gte: String
  type_contains: String
  type_not_contains: String
  type_starts_with: String
  type_not_starts_with: String
  type_ends_with: String
  type_not_ends_with: String
  user: UserWhereInput
  AND: [NotificationWhereInput!]
  OR: [NotificationWhereInput!]
  NOT: [NotificationWhereInput!]
}

input NotificationWhereUniqueInput {
  id: ID
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

enum Permission {
  ADMIN
  USER
  POLITICIANCREATE
  POLITICIANUPDATE
  POLITICIANDELETE
  PERMISSIONUPDATE
}

type Politician {
  id: ID!
  party: String
  name: String!
  title: String
  chamber: String
  state: String
  district: Int
  nthCongress: String
  phone: String
  gender: String
  image: String
  largeImage: String
  website: String
  govUrl: String
  createdAt: DateTime!
  updatedAt: DateTime!
  followers: User
  bills(where: BillWhereInput, orderBy: BillOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Bill!]
  coBills(where: BillWhereInput, orderBy: BillOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Bill!]
  mentions(where: CommentWhereInput, orderBy: CommentOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Comment!]
}

type PoliticianConnection {
  pageInfo: PageInfo!
  edges: [PoliticianEdge]!
  aggregate: AggregatePolitician!
}

input PoliticianCreateInput {
  party: String
  name: String!
  title: String
  chamber: String
  state: String
  district: Int
  nthCongress: String
  phone: String
  gender: String
  image: String
  largeImage: String
  website: String
  govUrl: String
  followers: UserCreateOneWithoutMyPoliticiansInput
  bills: BillCreateManyInput
  coBills: BillCreateManyWithoutCoSponsorsInput
  mentions: CommentCreateManyWithoutPoliticiansMentionedInput
}

input PoliticianCreateManyInput {
  create: [PoliticianCreateInput!]
  connect: [PoliticianWhereUniqueInput!]
}

input PoliticianCreateManyWithoutCoBillsInput {
  create: [PoliticianCreateWithoutCoBillsInput!]
  connect: [PoliticianWhereUniqueInput!]
}

input PoliticianCreateManyWithoutFollowersInput {
  create: [PoliticianCreateWithoutFollowersInput!]
  connect: [PoliticianWhereUniqueInput!]
}

input PoliticianCreateManyWithoutMentionsInput {
  create: [PoliticianCreateWithoutMentionsInput!]
  connect: [PoliticianWhereUniqueInput!]
}

input PoliticianCreateWithoutCoBillsInput {
  party: String
  name: String!
  title: String
  chamber: String
  state: String
  district: Int
  nthCongress: String
  phone: String
  gender: String
  image: String
  largeImage: String
  website: String
  govUrl: String
  followers: UserCreateOneWithoutMyPoliticiansInput
  bills: BillCreateManyInput
  mentions: CommentCreateManyWithoutPoliticiansMentionedInput
}

input PoliticianCreateWithoutFollowersInput {
  party: String
  name: String!
  title: String
  chamber: String
  state: String
  district: Int
  nthCongress: String
  phone: String
  gender: String
  image: String
  largeImage: String
  website: String
  govUrl: String
  bills: BillCreateManyInput
  coBills: BillCreateManyWithoutCoSponsorsInput
  mentions: CommentCreateManyWithoutPoliticiansMentionedInput
}

input PoliticianCreateWithoutMentionsInput {
  party: String
  name: String!
  title: String
  chamber: String
  state: String
  district: Int
  nthCongress: String
  phone: String
  gender: String
  image: String
  largeImage: String
  website: String
  govUrl: String
  followers: UserCreateOneWithoutMyPoliticiansInput
  bills: BillCreateManyInput
  coBills: BillCreateManyWithoutCoSponsorsInput
}

type PoliticianEdge {
  node: Politician!
  cursor: String!
}

enum PoliticianOrderByInput {
  id_ASC
  id_DESC
  party_ASC
  party_DESC
  name_ASC
  name_DESC
  title_ASC
  title_DESC
  chamber_ASC
  chamber_DESC
  state_ASC
  state_DESC
  district_ASC
  district_DESC
  nthCongress_ASC
  nthCongress_DESC
  phone_ASC
  phone_DESC
  gender_ASC
  gender_DESC
  image_ASC
  image_DESC
  largeImage_ASC
  largeImage_DESC
  website_ASC
  website_DESC
  govUrl_ASC
  govUrl_DESC
  createdAt_ASC
  createdAt_DESC
  updatedAt_ASC
  updatedAt_DESC
}

input PoliticianScalarWhereInput {
  id: ID
  id_not: ID
  id_in: [ID!]
  id_not_in: [ID!]
  id_lt: ID
  id_lte: ID
  id_gt: ID
  id_gte: ID
  id_contains: ID
  id_not_contains: ID
  id_starts_with: ID
  id_not_starts_with: ID
  id_ends_with: ID
  id_not_ends_with: ID
  party: String
  party_not: String
  party_in: [String!]
  party_not_in: [String!]
  party_lt: String
  party_lte: String
  party_gt: String
  party_gte: String
  party_contains: String
  party_not_contains: String
  party_starts_with: String
  party_not_starts_with: String
  party_ends_with: String
  party_not_ends_with: String
  name: String
  name_not: String
  name_in: [String!]
  name_not_in: [String!]
  name_lt: String
  name_lte: String
  name_gt: String
  name_gte: String
  name_contains: String
  name_not_contains: String
  name_starts_with: String
  name_not_starts_with: String
  name_ends_with: String
  name_not_ends_with: String
  title: String
  title_not: String
  title_in: [String!]
  title_not_in: [String!]
  title_lt: String
  title_lte: String
  title_gt: String
  title_gte: String
  title_contains: String
  title_not_contains: String
  title_starts_with: String
  title_not_starts_with: String
  title_ends_with: String
  title_not_ends_with: String
  chamber: String
  chamber_not: String
  chamber_in: [String!]
  chamber_not_in: [String!]
  chamber_lt: String
  chamber_lte: String
  chamber_gt: String
  chamber_gte: String
  chamber_contains: String
  chamber_not_contains: String
  chamber_starts_with: String
  chamber_not_starts_with: String
  chamber_ends_with: String
  chamber_not_ends_with: String
  state: String
  state_not: String
  state_in: [String!]
  state_not_in: [String!]
  state_lt: String
  state_lte: String
  state_gt: String
  state_gte: String
  state_contains: String
  state_not_contains: String
  state_starts_with: String
  state_not_starts_with: String
  state_ends_with: String
  state_not_ends_with: String
  district: Int
  district_not: Int
  district_in: [Int!]
  district_not_in: [Int!]
  district_lt: Int
  district_lte: Int
  district_gt: Int
  district_gte: Int
  nthCongress: String
  nthCongress_not: String
  nthCongress_in: [String!]
  nthCongress_not_in: [String!]
  nthCongress_lt: String
  nthCongress_lte: String
  nthCongress_gt: String
  nthCongress_gte: String
  nthCongress_contains: String
  nthCongress_not_contains: String
  nthCongress_starts_with: String
  nthCongress_not_starts_with: String
  nthCongress_ends_with: String
  nthCongress_not_ends_with: String
  phone: String
  phone_not: String
  phone_in: [String!]
  phone_not_in: [String!]
  phone_lt: String
  phone_lte: String
  phone_gt: String
  phone_gte: String
  phone_contains: String
  phone_not_contains: String
  phone_starts_with: String
  phone_not_starts_with: String
  phone_ends_with: String
  phone_not_ends_with: String
  gender: String
  gender_not: String
  gender_in: [String!]
  gender_not_in: [String!]
  gender_lt: String
  gender_lte: String
  gender_gt: String
  gender_gte: String
  gender_contains: String
  gender_not_contains: String
  gender_starts_with: String
  gender_not_starts_with: String
  gender_ends_with: String
  gender_not_ends_with: String
  image: String
  image_not: String
  image_in: [String!]
  image_not_in: [String!]
  image_lt: String
  image_lte: String
  image_gt: String
  image_gte: String
  image_contains: String
  image_not_contains: String
  image_starts_with: String
  image_not_starts_with: String
  image_ends_with: String
  image_not_ends_with: String
  largeImage: String
  largeImage_not: String
  largeImage_in: [String!]
  largeImage_not_in: [String!]
  largeImage_lt: String
  largeImage_lte: String
  largeImage_gt: String
  largeImage_gte: String
  largeImage_contains: String
  largeImage_not_contains: String
  largeImage_starts_with: String
  largeImage_not_starts_with: String
  largeImage_ends_with: String
  largeImage_not_ends_with: String
  website: String
  website_not: String
  website_in: [String!]
  website_not_in: [String!]
  website_lt: String
  website_lte: String
  website_gt: String
  website_gte: String
  website_contains: String
  website_not_contains: String
  website_starts_with: String
  website_not_starts_with: String
  website_ends_with: String
  website_not_ends_with: String
  govUrl: String
  govUrl_not: String
  govUrl_in: [String!]
  govUrl_not_in: [String!]
  govUrl_lt: String
  govUrl_lte: String
  govUrl_gt: String
  govUrl_gte: String
  govUrl_contains: String
  govUrl_not_contains: String
  govUrl_starts_with: String
  govUrl_not_starts_with: String
  govUrl_ends_with: String
  govUrl_not_ends_with: String
  createdAt: DateTime
  createdAt_not: DateTime
  createdAt_in: [DateTime!]
  createdAt_not_in: [DateTime!]
  createdAt_lt: DateTime
  createdAt_lte: DateTime
  createdAt_gt: DateTime
  createdAt_gte: DateTime
  updatedAt: DateTime
  updatedAt_not: DateTime
  updatedAt_in: [DateTime!]
  updatedAt_not_in: [DateTime!]
  updatedAt_lt: DateTime
  updatedAt_lte: DateTime
  updatedAt_gt: DateTime
  updatedAt_gte: DateTime
  AND: [PoliticianScalarWhereInput!]
  OR: [PoliticianScalarWhereInput!]
  NOT: [PoliticianScalarWhereInput!]
}

input PoliticianUpdateInput {
  party: String
  name: String
  title: String
  chamber: String
  state: String
  district: Int
  nthCongress: String
  phone: String
  gender: String
  image: String
  largeImage: String
  website: String
  govUrl: String
  followers: UserUpdateOneWithoutMyPoliticiansInput
  bills: BillUpdateManyInput
  coBills: BillUpdateManyWithoutCoSponsorsInput
  mentions: CommentUpdateManyWithoutPoliticiansMentionedInput
}

input PoliticianUpdateManyDataInput {
  party: String
  name: String
  title: String
  chamber: String
  state: String
  district: Int
  nthCongress: String
  phone: String
  gender: String
  image: String
  largeImage: String
  website: String
  govUrl: String
}

input PoliticianUpdateManyMutationInput {
  party: String
  name: String
  title: String
  chamber: String
  state: String
  district: Int
  nthCongress: String
  phone: String
  gender: String
  image: String
  largeImage: String
  website: String
  govUrl: String
}

input PoliticianUpdateManyWithoutCoBillsInput {
  create: [PoliticianCreateWithoutCoBillsInput!]
  delete: [PoliticianWhereUniqueInput!]
  connect: [PoliticianWhereUniqueInput!]
  disconnect: [PoliticianWhereUniqueInput!]
  update: [PoliticianUpdateWithWhereUniqueWithoutCoBillsInput!]
  upsert: [PoliticianUpsertWithWhereUniqueWithoutCoBillsInput!]
  deleteMany: [PoliticianScalarWhereInput!]
  updateMany: [PoliticianUpdateManyWithWhereNestedInput!]
}

input PoliticianUpdateManyWithoutFollowersInput {
  create: [PoliticianCreateWithoutFollowersInput!]
  delete: [PoliticianWhereUniqueInput!]
  connect: [PoliticianWhereUniqueInput!]
  disconnect: [PoliticianWhereUniqueInput!]
  update: [PoliticianUpdateWithWhereUniqueWithoutFollowersInput!]
  upsert: [PoliticianUpsertWithWhereUniqueWithoutFollowersInput!]
  deleteMany: [PoliticianScalarWhereInput!]
  updateMany: [PoliticianUpdateManyWithWhereNestedInput!]
}

input PoliticianUpdateManyWithoutMentionsInput {
  create: [PoliticianCreateWithoutMentionsInput!]
  delete: [PoliticianWhereUniqueInput!]
  connect: [PoliticianWhereUniqueInput!]
  disconnect: [PoliticianWhereUniqueInput!]
  update: [PoliticianUpdateWithWhereUniqueWithoutMentionsInput!]
  upsert: [PoliticianUpsertWithWhereUniqueWithoutMentionsInput!]
  deleteMany: [PoliticianScalarWhereInput!]
  updateMany: [PoliticianUpdateManyWithWhereNestedInput!]
}

input PoliticianUpdateManyWithWhereNestedInput {
  where: PoliticianScalarWhereInput!
  data: PoliticianUpdateManyDataInput!
}

input PoliticianUpdateWithoutCoBillsDataInput {
  party: String
  name: String
  title: String
  chamber: String
  state: String
  district: Int
  nthCongress: String
  phone: String
  gender: String
  image: String
  largeImage: String
  website: String
  govUrl: String
  followers: UserUpdateOneWithoutMyPoliticiansInput
  bills: BillUpdateManyInput
  mentions: CommentUpdateManyWithoutPoliticiansMentionedInput
}

input PoliticianUpdateWithoutFollowersDataInput {
  party: String
  name: String
  title: String
  chamber: String
  state: String
  district: Int
  nthCongress: String
  phone: String
  gender: String
  image: String
  largeImage: String
  website: String
  govUrl: String
  bills: BillUpdateManyInput
  coBills: BillUpdateManyWithoutCoSponsorsInput
  mentions: CommentUpdateManyWithoutPoliticiansMentionedInput
}

input PoliticianUpdateWithoutMentionsDataInput {
  party: String
  name: String
  title: String
  chamber: String
  state: String
  district: Int
  nthCongress: String
  phone: String
  gender: String
  image: String
  largeImage: String
  website: String
  govUrl: String
  followers: UserUpdateOneWithoutMyPoliticiansInput
  bills: BillUpdateManyInput
  coBills: BillUpdateManyWithoutCoSponsorsInput
}

input PoliticianUpdateWithWhereUniqueWithoutCoBillsInput {
  where: PoliticianWhereUniqueInput!
  data: PoliticianUpdateWithoutCoBillsDataInput!
}

input PoliticianUpdateWithWhereUniqueWithoutFollowersInput {
  where: PoliticianWhereUniqueInput!
  data: PoliticianUpdateWithoutFollowersDataInput!
}

input PoliticianUpdateWithWhereUniqueWithoutMentionsInput {
  where: PoliticianWhereUniqueInput!
  data: PoliticianUpdateWithoutMentionsDataInput!
}

input PoliticianUpsertWithWhereUniqueWithoutCoBillsInput {
  where: PoliticianWhereUniqueInput!
  update: PoliticianUpdateWithoutCoBillsDataInput!
  create: PoliticianCreateWithoutCoBillsInput!
}

input PoliticianUpsertWithWhereUniqueWithoutFollowersInput {
  where: PoliticianWhereUniqueInput!
  update: PoliticianUpdateWithoutFollowersDataInput!
  create: PoliticianCreateWithoutFollowersInput!
}

input PoliticianUpsertWithWhereUniqueWithoutMentionsInput {
  where: PoliticianWhereUniqueInput!
  update: PoliticianUpdateWithoutMentionsDataInput!
  create: PoliticianCreateWithoutMentionsInput!
}

input PoliticianWhereInput {
  id: ID
  id_not: ID
  id_in: [ID!]
  id_not_in: [ID!]
  id_lt: ID
  id_lte: ID
  id_gt: ID
  id_gte: ID
  id_contains: ID
  id_not_contains: ID
  id_starts_with: ID
  id_not_starts_with: ID
  id_ends_with: ID
  id_not_ends_with: ID
  party: String
  party_not: String
  party_in: [String!]
  party_not_in: [String!]
  party_lt: String
  party_lte: String
  party_gt: String
  party_gte: String
  party_contains: String
  party_not_contains: String
  party_starts_with: String
  party_not_starts_with: String
  party_ends_with: String
  party_not_ends_with: String
  name: String
  name_not: String
  name_in: [String!]
  name_not_in: [String!]
  name_lt: String
  name_lte: String
  name_gt: String
  name_gte: String
  name_contains: String
  name_not_contains: String
  name_starts_with: String
  name_not_starts_with: String
  name_ends_with: String
  name_not_ends_with: String
  title: String
  title_not: String
  title_in: [String!]
  title_not_in: [String!]
  title_lt: String
  title_lte: String
  title_gt: String
  title_gte: String
  title_contains: String
  title_not_contains: String
  title_starts_with: String
  title_not_starts_with: String
  title_ends_with: String
  title_not_ends_with: String
  chamber: String
  chamber_not: String
  chamber_in: [String!]
  chamber_not_in: [String!]
  chamber_lt: String
  chamber_lte: String
  chamber_gt: String
  chamber_gte: String
  chamber_contains: String
  chamber_not_contains: String
  chamber_starts_with: String
  chamber_not_starts_with: String
  chamber_ends_with: String
  chamber_not_ends_with: String
  state: String
  state_not: String
  state_in: [String!]
  state_not_in: [String!]
  state_lt: String
  state_lte: String
  state_gt: String
  state_gte: String
  state_contains: String
  state_not_contains: String
  state_starts_with: String
  state_not_starts_with: String
  state_ends_with: String
  state_not_ends_with: String
  district: Int
  district_not: Int
  district_in: [Int!]
  district_not_in: [Int!]
  district_lt: Int
  district_lte: Int
  district_gt: Int
  district_gte: Int
  nthCongress: String
  nthCongress_not: String
  nthCongress_in: [String!]
  nthCongress_not_in: [String!]
  nthCongress_lt: String
  nthCongress_lte: String
  nthCongress_gt: String
  nthCongress_gte: String
  nthCongress_contains: String
  nthCongress_not_contains: String
  nthCongress_starts_with: String
  nthCongress_not_starts_with: String
  nthCongress_ends_with: String
  nthCongress_not_ends_with: String
  phone: String
  phone_not: String
  phone_in: [String!]
  phone_not_in: [String!]
  phone_lt: String
  phone_lte: String
  phone_gt: String
  phone_gte: String
  phone_contains: String
  phone_not_contains: String
  phone_starts_with: String
  phone_not_starts_with: String
  phone_ends_with: String
  phone_not_ends_with: String
  gender: String
  gender_not: String
  gender_in: [String!]
  gender_not_in: [String!]
  gender_lt: String
  gender_lte: String
  gender_gt: String
  gender_gte: String
  gender_contains: String
  gender_not_contains: String
  gender_starts_with: String
  gender_not_starts_with: String
  gender_ends_with: String
  gender_not_ends_with: String
  image: String
  image_not: String
  image_in: [String!]
  image_not_in: [String!]
  image_lt: String
  image_lte: String
  image_gt: String
  image_gte: String
  image_contains: String
  image_not_contains: String
  image_starts_with: String
  image_not_starts_with: String
  image_ends_with: String
  image_not_ends_with: String
  largeImage: String
  largeImage_not: String
  largeImage_in: [String!]
  largeImage_not_in: [String!]
  largeImage_lt: String
  largeImage_lte: String
  largeImage_gt: String
  largeImage_gte: String
  largeImage_contains: String
  largeImage_not_contains: String
  largeImage_starts_with: String
  largeImage_not_starts_with: String
  largeImage_ends_with: String
  largeImage_not_ends_with: String
  website: String
  website_not: String
  website_in: [String!]
  website_not_in: [String!]
  website_lt: String
  website_lte: String
  website_gt: String
  website_gte: String
  website_contains: String
  website_not_contains: String
  website_starts_with: String
  website_not_starts_with: String
  website_ends_with: String
  website_not_ends_with: String
  govUrl: String
  govUrl_not: String
  govUrl_in: [String!]
  govUrl_not_in: [String!]
  govUrl_lt: String
  govUrl_lte: String
  govUrl_gt: String
  govUrl_gte: String
  govUrl_contains: String
  govUrl_not_contains: String
  govUrl_starts_with: String
  govUrl_not_starts_with: String
  govUrl_ends_with: String
  govUrl_not_ends_with: String
  createdAt: DateTime
  createdAt_not: DateTime
  createdAt_in: [DateTime!]
  createdAt_not_in: [DateTime!]
  createdAt_lt: DateTime
  createdAt_lte: DateTime
  createdAt_gt: DateTime
  createdAt_gte: DateTime
  updatedAt: DateTime
  updatedAt_not: DateTime
  updatedAt_in: [DateTime!]
  updatedAt_not_in: [DateTime!]
  updatedAt_lt: DateTime
  updatedAt_lte: DateTime
  updatedAt_gt: DateTime
  updatedAt_gte: DateTime
  followers: UserWhereInput
  bills_every: BillWhereInput
  bills_some: BillWhereInput
  bills_none: BillWhereInput
  coBills_every: BillWhereInput
  coBills_some: BillWhereInput
  coBills_none: BillWhereInput
  mentions_every: CommentWhereInput
  mentions_some: CommentWhereInput
  mentions_none: CommentWhereInput
  AND: [PoliticianWhereInput!]
  OR: [PoliticianWhereInput!]
  NOT: [PoliticianWhereInput!]
}

input PoliticianWhereUniqueInput {
  id: ID
  name: String
}

type Query {
  bill(where: BillWhereUniqueInput!): Bill
  bills(where: BillWhereInput, orderBy: BillOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Bill]!
  billsConnection(where: BillWhereInput, orderBy: BillOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): BillConnection!
  comment(where: CommentWhereUniqueInput!): Comment
  comments(where: CommentWhereInput, orderBy: CommentOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Comment]!
  commentsConnection(where: CommentWhereInput, orderBy: CommentOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): CommentConnection!
  feeds(where: FeedWhereInput, orderBy: FeedOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Feed]!
  feedsConnection(where: FeedWhereInput, orderBy: FeedOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): FeedConnection!
  notification(where: NotificationWhereUniqueInput!): Notification
  notifications(where: NotificationWhereInput, orderBy: NotificationOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Notification]!
  notificationsConnection(where: NotificationWhereInput, orderBy: NotificationOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): NotificationConnection!
  politician(where: PoliticianWhereUniqueInput!): Politician
  politicians(where: PoliticianWhereInput, orderBy: PoliticianOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Politician]!
  politiciansConnection(where: PoliticianWhereInput, orderBy: PoliticianOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): PoliticianConnection!
  subscriptions(where: SubscriptionWhereInput, orderBy: SubscriptionOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Subscription]!
  subscriptionsConnection(where: SubscriptionWhereInput, orderBy: SubscriptionOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): SubscriptionConnection!
  topic(where: TopicWhereUniqueInput!): Topic
  topics(where: TopicWhereInput, orderBy: TopicOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Topic]!
  topicsConnection(where: TopicWhereInput, orderBy: TopicOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): TopicConnection!
  user(where: UserWhereUniqueInput!): User
  users(where: UserWhereInput, orderBy: UserOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [User]!
  usersConnection(where: UserWhereInput, orderBy: UserOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): UserConnection!
  node(id: ID!): Node
}

type Subscription {
  newBillComment: Comment
  newBill: Bill
}

type SubscriptionConnection {
  pageInfo: PageInfo!
  edges: [SubscriptionEdge]!
  aggregate: AggregateSubscription!
}

input SubscriptionCreateInput {
  newBillComment: CommentCreateOneInput
  newBill: BillCreateOneInput
}

type SubscriptionEdge {
  node: Subscription!
  cursor: String!
}

enum SubscriptionOrderByInput {
  id_ASC
  id_DESC
  createdAt_ASC
  createdAt_DESC
  updatedAt_ASC
  updatedAt_DESC
}

input SubscriptionWhereInput {
  newBillComment: CommentWhereInput
  newBill: BillWhereInput
  AND: [SubscriptionWhereInput!]
  OR: [SubscriptionWhereInput!]
  NOT: [SubscriptionWhereInput!]
}

type Topic {
  id: ID!
  title: String
  comments(where: CommentWhereInput, orderBy: CommentOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Comment!]
  commenters(where: UserWhereInput, orderBy: UserOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [User!]
}

type TopicConnection {
  pageInfo: PageInfo!
  edges: [TopicEdge]!
  aggregate: AggregateTopic!
}

input TopicCreateInput {
  title: String
  comments: CommentCreateManyWithoutTopicInput
  commenters: UserCreateManyWithoutTopicCommentsInput
}

input TopicCreateManyWithoutCommentersInput {
  create: [TopicCreateWithoutCommentersInput!]
  connect: [TopicWhereUniqueInput!]
}

input TopicCreateOneWithoutCommentsInput {
  create: TopicCreateWithoutCommentsInput
  connect: TopicWhereUniqueInput
}

input TopicCreateWithoutCommentersInput {
  title: String
  comments: CommentCreateManyWithoutTopicInput
}

input TopicCreateWithoutCommentsInput {
  title: String
  commenters: UserCreateManyWithoutTopicCommentsInput
}

type TopicEdge {
  node: Topic!
  cursor: String!
}

enum TopicOrderByInput {
  id_ASC
  id_DESC
  title_ASC
  title_DESC
  createdAt_ASC
  createdAt_DESC
  updatedAt_ASC
  updatedAt_DESC
}

input TopicScalarWhereInput {
  id: ID
  id_not: ID
  id_in: [ID!]
  id_not_in: [ID!]
  id_lt: ID
  id_lte: ID
  id_gt: ID
  id_gte: ID
  id_contains: ID
  id_not_contains: ID
  id_starts_with: ID
  id_not_starts_with: ID
  id_ends_with: ID
  id_not_ends_with: ID
  title: String
  title_not: String
  title_in: [String!]
  title_not_in: [String!]
  title_lt: String
  title_lte: String
  title_gt: String
  title_gte: String
  title_contains: String
  title_not_contains: String
  title_starts_with: String
  title_not_starts_with: String
  title_ends_with: String
  title_not_ends_with: String
  AND: [TopicScalarWhereInput!]
  OR: [TopicScalarWhereInput!]
  NOT: [TopicScalarWhereInput!]
}

input TopicUpdateInput {
  title: String
  comments: CommentUpdateManyWithoutTopicInput
  commenters: UserUpdateManyWithoutTopicCommentsInput
}

input TopicUpdateManyDataInput {
  title: String
}

input TopicUpdateManyMutationInput {
  title: String
}

input TopicUpdateManyWithoutCommentersInput {
  create: [TopicCreateWithoutCommentersInput!]
  delete: [TopicWhereUniqueInput!]
  connect: [TopicWhereUniqueInput!]
  disconnect: [TopicWhereUniqueInput!]
  update: [TopicUpdateWithWhereUniqueWithoutCommentersInput!]
  upsert: [TopicUpsertWithWhereUniqueWithoutCommentersInput!]
  deleteMany: [TopicScalarWhereInput!]
  updateMany: [TopicUpdateManyWithWhereNestedInput!]
}

input TopicUpdateManyWithWhereNestedInput {
  where: TopicScalarWhereInput!
  data: TopicUpdateManyDataInput!
}

input TopicUpdateOneWithoutCommentsInput {
  create: TopicCreateWithoutCommentsInput
  update: TopicUpdateWithoutCommentsDataInput
  upsert: TopicUpsertWithoutCommentsInput
  delete: Boolean
  disconnect: Boolean
  connect: TopicWhereUniqueInput
}

input TopicUpdateWithoutCommentersDataInput {
  title: String
  comments: CommentUpdateManyWithoutTopicInput
}

input TopicUpdateWithoutCommentsDataInput {
  title: String
  commenters: UserUpdateManyWithoutTopicCommentsInput
}

input TopicUpdateWithWhereUniqueWithoutCommentersInput {
  where: TopicWhereUniqueInput!
  data: TopicUpdateWithoutCommentersDataInput!
}

input TopicUpsertWithoutCommentsInput {
  update: TopicUpdateWithoutCommentsDataInput!
  create: TopicCreateWithoutCommentsInput!
}

input TopicUpsertWithWhereUniqueWithoutCommentersInput {
  where: TopicWhereUniqueInput!
  update: TopicUpdateWithoutCommentersDataInput!
  create: TopicCreateWithoutCommentersInput!
}

input TopicWhereInput {
  id: ID
  id_not: ID
  id_in: [ID!]
  id_not_in: [ID!]
  id_lt: ID
  id_lte: ID
  id_gt: ID
  id_gte: ID
  id_contains: ID
  id_not_contains: ID
  id_starts_with: ID
  id_not_starts_with: ID
  id_ends_with: ID
  id_not_ends_with: ID
  title: String
  title_not: String
  title_in: [String!]
  title_not_in: [String!]
  title_lt: String
  title_lte: String
  title_gt: String
  title_gte: String
  title_contains: String
  title_not_contains: String
  title_starts_with: String
  title_not_starts_with: String
  title_ends_with: String
  title_not_ends_with: String
  comments_every: CommentWhereInput
  comments_some: CommentWhereInput
  comments_none: CommentWhereInput
  commenters_every: UserWhereInput
  commenters_some: UserWhereInput
  commenters_none: UserWhereInput
  AND: [TopicWhereInput!]
  OR: [TopicWhereInput!]
  NOT: [TopicWhereInput!]
}

input TopicWhereUniqueInput {
  id: ID
}

type User {
  id: ID!
  name: String!
  email: String!
  password: String
  permissions: [Permission!]!
  myPoliticians(where: PoliticianWhereInput, orderBy: PoliticianOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Politician!]
  myBills(where: BillWhereInput, orderBy: BillOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Bill!]
  upvotedBills(where: BillWhereInput, orderBy: BillOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Bill!]
  downvotedBills(where: BillWhereInput, orderBy: BillOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Bill!]
  billComments(where: CommentWhereInput, orderBy: CommentOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Comment!]
  topicComments(where: TopicWhereInput, orderBy: TopicOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Topic!]
  notifications(where: NotificationWhereInput, orderBy: NotificationOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Notification!]
}

type UserConnection {
  pageInfo: PageInfo!
  edges: [UserEdge]!
  aggregate: AggregateUser!
}

input UserCreateInput {
  name: String!
  email: String!
  password: String
  permissions: UserCreatepermissionsInput
  myPoliticians: PoliticianCreateManyWithoutFollowersInput
  myBills: BillCreateManyWithoutFollowersInput
  upvotedBills: BillCreateManyWithoutUpvotesInput
  downvotedBills: BillCreateManyWithoutDownvotesInput
  billComments: CommentCreateManyWithoutAuthorInput
  topicComments: TopicCreateManyWithoutCommentersInput
  notifications: NotificationCreateManyWithoutUserInput
}

input UserCreateManyWithoutDownvotedBillsInput {
  create: [UserCreateWithoutDownvotedBillsInput!]
  connect: [UserWhereUniqueInput!]
}

input UserCreateManyWithoutMyBillsInput {
  create: [UserCreateWithoutMyBillsInput!]
  connect: [UserWhereUniqueInput!]
}

input UserCreateManyWithoutTopicCommentsInput {
  create: [UserCreateWithoutTopicCommentsInput!]
  connect: [UserWhereUniqueInput!]
}

input UserCreateManyWithoutUpvotedBillsInput {
  create: [UserCreateWithoutUpvotedBillsInput!]
  connect: [UserWhereUniqueInput!]
}

input UserCreateOneWithoutBillCommentsInput {
  create: UserCreateWithoutBillCommentsInput
  connect: UserWhereUniqueInput
}

input UserCreateOneWithoutMyPoliticiansInput {
  create: UserCreateWithoutMyPoliticiansInput
  connect: UserWhereUniqueInput
}

input UserCreateOneWithoutNotificationsInput {
  create: UserCreateWithoutNotificationsInput
  connect: UserWhereUniqueInput
}

input UserCreatepermissionsInput {
  set: [Permission!]
}

input UserCreateWithoutBillCommentsInput {
  name: String!
  email: String!
  password: String
  permissions: UserCreatepermissionsInput
  myPoliticians: PoliticianCreateManyWithoutFollowersInput
  myBills: BillCreateManyWithoutFollowersInput
  upvotedBills: BillCreateManyWithoutUpvotesInput
  downvotedBills: BillCreateManyWithoutDownvotesInput
  topicComments: TopicCreateManyWithoutCommentersInput
  notifications: NotificationCreateManyWithoutUserInput
}

input UserCreateWithoutDownvotedBillsInput {
  name: String!
  email: String!
  password: String
  permissions: UserCreatepermissionsInput
  myPoliticians: PoliticianCreateManyWithoutFollowersInput
  myBills: BillCreateManyWithoutFollowersInput
  upvotedBills: BillCreateManyWithoutUpvotesInput
  billComments: CommentCreateManyWithoutAuthorInput
  topicComments: TopicCreateManyWithoutCommentersInput
  notifications: NotificationCreateManyWithoutUserInput
}

input UserCreateWithoutMyBillsInput {
  name: String!
  email: String!
  password: String
  permissions: UserCreatepermissionsInput
  myPoliticians: PoliticianCreateManyWithoutFollowersInput
  upvotedBills: BillCreateManyWithoutUpvotesInput
  downvotedBills: BillCreateManyWithoutDownvotesInput
  billComments: CommentCreateManyWithoutAuthorInput
  topicComments: TopicCreateManyWithoutCommentersInput
  notifications: NotificationCreateManyWithoutUserInput
}

input UserCreateWithoutMyPoliticiansInput {
  name: String!
  email: String!
  password: String
  permissions: UserCreatepermissionsInput
  myBills: BillCreateManyWithoutFollowersInput
  upvotedBills: BillCreateManyWithoutUpvotesInput
  downvotedBills: BillCreateManyWithoutDownvotesInput
  billComments: CommentCreateManyWithoutAuthorInput
  topicComments: TopicCreateManyWithoutCommentersInput
  notifications: NotificationCreateManyWithoutUserInput
}

input UserCreateWithoutNotificationsInput {
  name: String!
  email: String!
  password: String
  permissions: UserCreatepermissionsInput
  myPoliticians: PoliticianCreateManyWithoutFollowersInput
  myBills: BillCreateManyWithoutFollowersInput
  upvotedBills: BillCreateManyWithoutUpvotesInput
  downvotedBills: BillCreateManyWithoutDownvotesInput
  billComments: CommentCreateManyWithoutAuthorInput
  topicComments: TopicCreateManyWithoutCommentersInput
}

input UserCreateWithoutTopicCommentsInput {
  name: String!
  email: String!
  password: String
  permissions: UserCreatepermissionsInput
  myPoliticians: PoliticianCreateManyWithoutFollowersInput
  myBills: BillCreateManyWithoutFollowersInput
  upvotedBills: BillCreateManyWithoutUpvotesInput
  downvotedBills: BillCreateManyWithoutDownvotesInput
  billComments: CommentCreateManyWithoutAuthorInput
  notifications: NotificationCreateManyWithoutUserInput
}

input UserCreateWithoutUpvotedBillsInput {
  name: String!
  email: String!
  password: String
  permissions: UserCreatepermissionsInput
  myPoliticians: PoliticianCreateManyWithoutFollowersInput
  myBills: BillCreateManyWithoutFollowersInput
  downvotedBills: BillCreateManyWithoutDownvotesInput
  billComments: CommentCreateManyWithoutAuthorInput
  topicComments: TopicCreateManyWithoutCommentersInput
  notifications: NotificationCreateManyWithoutUserInput
}

type UserEdge {
  node: User!
  cursor: String!
}

enum UserOrderByInput {
  id_ASC
  id_DESC
  name_ASC
  name_DESC
  email_ASC
  email_DESC
  password_ASC
  password_DESC
  createdAt_ASC
  createdAt_DESC
  updatedAt_ASC
  updatedAt_DESC
}

input UserScalarWhereInput {
  id: ID
  id_not: ID
  id_in: [ID!]
  id_not_in: [ID!]
  id_lt: ID
  id_lte: ID
  id_gt: ID
  id_gte: ID
  id_contains: ID
  id_not_contains: ID
  id_starts_with: ID
  id_not_starts_with: ID
  id_ends_with: ID
  id_not_ends_with: ID
  name: String
  name_not: String
  name_in: [String!]
  name_not_in: [String!]
  name_lt: String
  name_lte: String
  name_gt: String
  name_gte: String
  name_contains: String
  name_not_contains: String
  name_starts_with: String
  name_not_starts_with: String
  name_ends_with: String
  name_not_ends_with: String
  email: String
  email_not: String
  email_in: [String!]
  email_not_in: [String!]
  email_lt: String
  email_lte: String
  email_gt: String
  email_gte: String
  email_contains: String
  email_not_contains: String
  email_starts_with: String
  email_not_starts_with: String
  email_ends_with: String
  email_not_ends_with: String
  password: String
  password_not: String
  password_in: [String!]
  password_not_in: [String!]
  password_lt: String
  password_lte: String
  password_gt: String
  password_gte: String
  password_contains: String
  password_not_contains: String
  password_starts_with: String
  password_not_starts_with: String
  password_ends_with: String
  password_not_ends_with: String
  AND: [UserScalarWhereInput!]
  OR: [UserScalarWhereInput!]
  NOT: [UserScalarWhereInput!]
}

input UserUpdateInput {
  name: String
  email: String
  password: String
  permissions: UserUpdatepermissionsInput
  myPoliticians: PoliticianUpdateManyWithoutFollowersInput
  myBills: BillUpdateManyWithoutFollowersInput
  upvotedBills: BillUpdateManyWithoutUpvotesInput
  downvotedBills: BillUpdateManyWithoutDownvotesInput
  billComments: CommentUpdateManyWithoutAuthorInput
  topicComments: TopicUpdateManyWithoutCommentersInput
  notifications: NotificationUpdateManyWithoutUserInput
}

input UserUpdateManyDataInput {
  name: String
  email: String
  password: String
  permissions: UserUpdatepermissionsInput
}

input UserUpdateManyMutationInput {
  name: String
  email: String
  password: String
  permissions: UserUpdatepermissionsInput
}

input UserUpdateManyWithoutDownvotedBillsInput {
  create: [UserCreateWithoutDownvotedBillsInput!]
  delete: [UserWhereUniqueInput!]
  connect: [UserWhereUniqueInput!]
  disconnect: [UserWhereUniqueInput!]
  update: [UserUpdateWithWhereUniqueWithoutDownvotedBillsInput!]
  upsert: [UserUpsertWithWhereUniqueWithoutDownvotedBillsInput!]
  deleteMany: [UserScalarWhereInput!]
  updateMany: [UserUpdateManyWithWhereNestedInput!]
}

input UserUpdateManyWithoutMyBillsInput {
  create: [UserCreateWithoutMyBillsInput!]
  delete: [UserWhereUniqueInput!]
  connect: [UserWhereUniqueInput!]
  disconnect: [UserWhereUniqueInput!]
  update: [UserUpdateWithWhereUniqueWithoutMyBillsInput!]
  upsert: [UserUpsertWithWhereUniqueWithoutMyBillsInput!]
  deleteMany: [UserScalarWhereInput!]
  updateMany: [UserUpdateManyWithWhereNestedInput!]
}

input UserUpdateManyWithoutTopicCommentsInput {
  create: [UserCreateWithoutTopicCommentsInput!]
  delete: [UserWhereUniqueInput!]
  connect: [UserWhereUniqueInput!]
  disconnect: [UserWhereUniqueInput!]
  update: [UserUpdateWithWhereUniqueWithoutTopicCommentsInput!]
  upsert: [UserUpsertWithWhereUniqueWithoutTopicCommentsInput!]
  deleteMany: [UserScalarWhereInput!]
  updateMany: [UserUpdateManyWithWhereNestedInput!]
}

input UserUpdateManyWithoutUpvotedBillsInput {
  create: [UserCreateWithoutUpvotedBillsInput!]
  delete: [UserWhereUniqueInput!]
  connect: [UserWhereUniqueInput!]
  disconnect: [UserWhereUniqueInput!]
  update: [UserUpdateWithWhereUniqueWithoutUpvotedBillsInput!]
  upsert: [UserUpsertWithWhereUniqueWithoutUpvotedBillsInput!]
  deleteMany: [UserScalarWhereInput!]
  updateMany: [UserUpdateManyWithWhereNestedInput!]
}

input UserUpdateManyWithWhereNestedInput {
  where: UserScalarWhereInput!
  data: UserUpdateManyDataInput!
}

input UserUpdateOneWithoutBillCommentsInput {
  create: UserCreateWithoutBillCommentsInput
  update: UserUpdateWithoutBillCommentsDataInput
  upsert: UserUpsertWithoutBillCommentsInput
  delete: Boolean
  disconnect: Boolean
  connect: UserWhereUniqueInput
}

input UserUpdateOneWithoutMyPoliticiansInput {
  create: UserCreateWithoutMyPoliticiansInput
  update: UserUpdateWithoutMyPoliticiansDataInput
  upsert: UserUpsertWithoutMyPoliticiansInput
  delete: Boolean
  disconnect: Boolean
  connect: UserWhereUniqueInput
}

input UserUpdateOneWithoutNotificationsInput {
  create: UserCreateWithoutNotificationsInput
  update: UserUpdateWithoutNotificationsDataInput
  upsert: UserUpsertWithoutNotificationsInput
  delete: Boolean
  disconnect: Boolean
  connect: UserWhereUniqueInput
}

input UserUpdatepermissionsInput {
  set: [Permission!]
}

input UserUpdateWithoutBillCommentsDataInput {
  name: String
  email: String
  password: String
  permissions: UserUpdatepermissionsInput
  myPoliticians: PoliticianUpdateManyWithoutFollowersInput
  myBills: BillUpdateManyWithoutFollowersInput
  upvotedBills: BillUpdateManyWithoutUpvotesInput
  downvotedBills: BillUpdateManyWithoutDownvotesInput
  topicComments: TopicUpdateManyWithoutCommentersInput
  notifications: NotificationUpdateManyWithoutUserInput
}

input UserUpdateWithoutDownvotedBillsDataInput {
  name: String
  email: String
  password: String
  permissions: UserUpdatepermissionsInput
  myPoliticians: PoliticianUpdateManyWithoutFollowersInput
  myBills: BillUpdateManyWithoutFollowersInput
  upvotedBills: BillUpdateManyWithoutUpvotesInput
  billComments: CommentUpdateManyWithoutAuthorInput
  topicComments: TopicUpdateManyWithoutCommentersInput
  notifications: NotificationUpdateManyWithoutUserInput
}

input UserUpdateWithoutMyBillsDataInput {
  name: String
  email: String
  password: String
  permissions: UserUpdatepermissionsInput
  myPoliticians: PoliticianUpdateManyWithoutFollowersInput
  upvotedBills: BillUpdateManyWithoutUpvotesInput
  downvotedBills: BillUpdateManyWithoutDownvotesInput
  billComments: CommentUpdateManyWithoutAuthorInput
  topicComments: TopicUpdateManyWithoutCommentersInput
  notifications: NotificationUpdateManyWithoutUserInput
}

input UserUpdateWithoutMyPoliticiansDataInput {
  name: String
  email: String
  password: String
  permissions: UserUpdatepermissionsInput
  myBills: BillUpdateManyWithoutFollowersInput
  upvotedBills: BillUpdateManyWithoutUpvotesInput
  downvotedBills: BillUpdateManyWithoutDownvotesInput
  billComments: CommentUpdateManyWithoutAuthorInput
  topicComments: TopicUpdateManyWithoutCommentersInput
  notifications: NotificationUpdateManyWithoutUserInput
}

input UserUpdateWithoutNotificationsDataInput {
  name: String
  email: String
  password: String
  permissions: UserUpdatepermissionsInput
  myPoliticians: PoliticianUpdateManyWithoutFollowersInput
  myBills: BillUpdateManyWithoutFollowersInput
  upvotedBills: BillUpdateManyWithoutUpvotesInput
  downvotedBills: BillUpdateManyWithoutDownvotesInput
  billComments: CommentUpdateManyWithoutAuthorInput
  topicComments: TopicUpdateManyWithoutCommentersInput
}

input UserUpdateWithoutTopicCommentsDataInput {
  name: String
  email: String
  password: String
  permissions: UserUpdatepermissionsInput
  myPoliticians: PoliticianUpdateManyWithoutFollowersInput
  myBills: BillUpdateManyWithoutFollowersInput
  upvotedBills: BillUpdateManyWithoutUpvotesInput
  downvotedBills: BillUpdateManyWithoutDownvotesInput
  billComments: CommentUpdateManyWithoutAuthorInput
  notifications: NotificationUpdateManyWithoutUserInput
}

input UserUpdateWithoutUpvotedBillsDataInput {
  name: String
  email: String
  password: String
  permissions: UserUpdatepermissionsInput
  myPoliticians: PoliticianUpdateManyWithoutFollowersInput
  myBills: BillUpdateManyWithoutFollowersInput
  downvotedBills: BillUpdateManyWithoutDownvotesInput
  billComments: CommentUpdateManyWithoutAuthorInput
  topicComments: TopicUpdateManyWithoutCommentersInput
  notifications: NotificationUpdateManyWithoutUserInput
}

input UserUpdateWithWhereUniqueWithoutDownvotedBillsInput {
  where: UserWhereUniqueInput!
  data: UserUpdateWithoutDownvotedBillsDataInput!
}

input UserUpdateWithWhereUniqueWithoutMyBillsInput {
  where: UserWhereUniqueInput!
  data: UserUpdateWithoutMyBillsDataInput!
}

input UserUpdateWithWhereUniqueWithoutTopicCommentsInput {
  where: UserWhereUniqueInput!
  data: UserUpdateWithoutTopicCommentsDataInput!
}

input UserUpdateWithWhereUniqueWithoutUpvotedBillsInput {
  where: UserWhereUniqueInput!
  data: UserUpdateWithoutUpvotedBillsDataInput!
}

input UserUpsertWithoutBillCommentsInput {
  update: UserUpdateWithoutBillCommentsDataInput!
  create: UserCreateWithoutBillCommentsInput!
}

input UserUpsertWithoutMyPoliticiansInput {
  update: UserUpdateWithoutMyPoliticiansDataInput!
  create: UserCreateWithoutMyPoliticiansInput!
}

input UserUpsertWithoutNotificationsInput {
  update: UserUpdateWithoutNotificationsDataInput!
  create: UserCreateWithoutNotificationsInput!
}

input UserUpsertWithWhereUniqueWithoutDownvotedBillsInput {
  where: UserWhereUniqueInput!
  update: UserUpdateWithoutDownvotedBillsDataInput!
  create: UserCreateWithoutDownvotedBillsInput!
}

input UserUpsertWithWhereUniqueWithoutMyBillsInput {
  where: UserWhereUniqueInput!
  update: UserUpdateWithoutMyBillsDataInput!
  create: UserCreateWithoutMyBillsInput!
}

input UserUpsertWithWhereUniqueWithoutTopicCommentsInput {
  where: UserWhereUniqueInput!
  update: UserUpdateWithoutTopicCommentsDataInput!
  create: UserCreateWithoutTopicCommentsInput!
}

input UserUpsertWithWhereUniqueWithoutUpvotedBillsInput {
  where: UserWhereUniqueInput!
  update: UserUpdateWithoutUpvotedBillsDataInput!
  create: UserCreateWithoutUpvotedBillsInput!
}

input UserWhereInput {
  id: ID
  id_not: ID
  id_in: [ID!]
  id_not_in: [ID!]
  id_lt: ID
  id_lte: ID
  id_gt: ID
  id_gte: ID
  id_contains: ID
  id_not_contains: ID
  id_starts_with: ID
  id_not_starts_with: ID
  id_ends_with: ID
  id_not_ends_with: ID
  name: String
  name_not: String
  name_in: [String!]
  name_not_in: [String!]
  name_lt: String
  name_lte: String
  name_gt: String
  name_gte: String
  name_contains: String
  name_not_contains: String
  name_starts_with: String
  name_not_starts_with: String
  name_ends_with: String
  name_not_ends_with: String
  email: String
  email_not: String
  email_in: [String!]
  email_not_in: [String!]
  email_lt: String
  email_lte: String
  email_gt: String
  email_gte: String
  email_contains: String
  email_not_contains: String
  email_starts_with: String
  email_not_starts_with: String
  email_ends_with: String
  email_not_ends_with: String
  password: String
  password_not: String
  password_in: [String!]
  password_not_in: [String!]
  password_lt: String
  password_lte: String
  password_gt: String
  password_gte: String
  password_contains: String
  password_not_contains: String
  password_starts_with: String
  password_not_starts_with: String
  password_ends_with: String
  password_not_ends_with: String
  myPoliticians_every: PoliticianWhereInput
  myPoliticians_some: PoliticianWhereInput
  myPoliticians_none: PoliticianWhereInput
  myBills_every: BillWhereInput
  myBills_some: BillWhereInput
  myBills_none: BillWhereInput
  upvotedBills_every: BillWhereInput
  upvotedBills_some: BillWhereInput
  upvotedBills_none: BillWhereInput
  downvotedBills_every: BillWhereInput
  downvotedBills_some: BillWhereInput
  downvotedBills_none: BillWhereInput
  billComments_every: CommentWhereInput
  billComments_some: CommentWhereInput
  billComments_none: CommentWhereInput
  topicComments_every: TopicWhereInput
  topicComments_some: TopicWhereInput
  topicComments_none: TopicWhereInput
  notifications_every: NotificationWhereInput
  notifications_some: NotificationWhereInput
  notifications_none: NotificationWhereInput
  AND: [UserWhereInput!]
  OR: [UserWhereInput!]
  NOT: [UserWhereInput!]
}

input UserWhereUniqueInput {
  id: ID
  email: String
}
`
      }
    
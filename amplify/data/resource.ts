import { type ClientSchema, a, defineData } from "@aws-amplify/backend";
import { postConfirmation } from "../auth/post-confirmation/resource";

const schema = a
  .schema({
    Cards: a
      .model({
        id: a.string().required(),
        expansion: a.customType({
          id: a.string().required(),
          name: a.string().required(),
          pack: a.string().required(),
          rates: a.customType({
            card1To3: a.float().required(),
            card4: a.float().required(),
            card5: a.float().required(),
          }),
        }),
        name: a.string().required(),
        rarity: a.string().required(),
      })
      .authorization(allow => [
        allow.publicApiKey()
      ]),

    UserProfile: a
      .model({
        email: a.string(),
        profileOwner: a.string(),
      })
      .authorization((allow) => [
        allow.ownerDefinedIn("profileOwner"),
      ]),
  })
  .authorization((allow) => [allow.resource(postConfirmation)]);
export type Schema = ClientSchema<typeof schema>;

export const data = defineData({
  schema,
  authorizationModes: {
    defaultAuthorizationMode: "apiKey",
    apiKeyAuthorizationMode: {
      expiresInDays: 30,
    },
  },
});

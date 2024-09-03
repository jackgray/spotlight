
export const supersetConfig = {
    supersetUrl: process.env.SUPERSET_URL || 'https://your-superset-endpoint.com',
    username: process.env.SUPERSET_USERNAME || 'admin',
    password: process.env.SUPERSET_PASSWORD || 'admin',
    guestUsername: process.env.SUPERSET_GUEST_USERNAME || 'guestUser',
    guestFirstName: process.env.SUPERSET_GUEST_FNAME || 'Guest',
    guestLastName: process.env.SUPERSET_GUEST_LNAME || 'User',
  };
  
  
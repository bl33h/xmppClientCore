require('dotenv').config();
const { client, xml } = require('@xmpp/client');

const xmpp = client({
  service: process.env.SERVICE_URL,
  domain: process.env.DOMAIN,
  resource: process.env.RESOURCE,
  username: process.env.USERNAMES,
  password: process.env.PASSWORD
});

xmpp.on('online', async (address) => {
  console.log('✔', 'connected as ->', address.toString());

  await xmpp.send(xml('presence'));
  console.log('presence sent');

  const message = xml(
    'message',
    { type: 'chat', to: '@alumchat.lol' },
    xml('body', {}, 'hello hello')
  );
  console.log('message created:', message.toString());

  await xmpp.send(message);
  console.log('✔ message sent');

  xmpp.stop();
});

xmpp.on('error', (err) => {
  console.error('!', 'connection error:', err);
});

xmpp.start().catch(console.error);
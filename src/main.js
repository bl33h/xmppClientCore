require('dotenv').config();
const { client, xml } = require('@xmpp/client');

// create a new xmpp client
const xmpp = client({
  service: process.env.SERVICE_URL,
  domain: process.env.DOMAIN,
  resource: process.env.RESOURCE,
  username: process.env.USERNAMES,
  password: process.env.PASSWORD
});

// connection
xmpp.on('online', async (address) => {
  console.log('✔', 'connected as ->', address.toString());

  await xmpp.send(xml('presence'));
  console.log('presence sent');

  const message = xml(
    'message',
    { type: 'chat', to: 'per21371@alumchat.lol' },
    xml('body', {}, 'hello hello')
  );
  console.log('message created:', message.toString());

  await xmpp.send(message);
  console.log('✔ message sent');
});

// replies
xmpp.on('stanza', (stanza) => {
  if (stanza.is('message') && stanza.getChild('body')) {
    const from = stanza.attrs.from;
    const body = stanza.getChild('body').text();
    console.log(`• you just got a message from [${from}]: ${body}`);
  }
});

// error management
xmpp.on('error', (err) => {
  console.error('!', 'connection error:', err);
});

xmpp.start().catch(console.error);
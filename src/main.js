const { client, xml } = require('@xmpp/client');

const xmpp = client({
  service: 'ws://alumchat.lol:7070/ws/',
  domain: 'alumchat.lol',
  resource: 'example',
  username: 'per21371',
  password: 'per21371'
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

xmpp.start().catch(console.error);
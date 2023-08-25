To start rabbitmq now and restart at login:
  brew services start rabbitmq
Or, if you don't want/need a background service you can just run:
  CONF_ENV_FILE="/usr/local/etc/rabbitmq/rabbitmq-env.conf" /usr/local/opt/rabbitmq/sbin/rabbitmq-server


open this:
  http://localhost:15672/

    Username: guest
    Password: guest

to check it from terminal:
1) nano ~/.zshrc # edit shell configuration
2) # Add RabbitMQ sbin directory to PATH 
   export PATH=$PATH:"/usr/local/Cellar/rabbitmq/3.12.2/sbin"
3) source ~/.zshrc #reload shell configurations
4) rabbitmqctl status #use rabbitmqctl cli tool

start and stop rabbit mq

  1) brew services start rabbitmq
  2) brew services stop rabbitmq


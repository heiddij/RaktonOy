class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];
    }

    display() {
        const {openButton, chatBox, sendButton} = this.args; // extract arguments

        openButton.addEventListener('click', () => this.toggleState(chatBox)); // when event click (open button), execute toggleSate()
        sendButton.addEventListener('click', () => this.onSendButton(chatBox)); // when event click (send button), execute onSendButton()

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => { // send the message when releasing enter (keyup)
            if (key === "Enter") {
                this.onSendButton(chatBox);
            }
        })
    }

    toggleState(chatbox) {
        this.state = !this.state;

        // show or hides the box
        if(this.state) {
            chatbox.classList.add('chatbox--active');
        }
        else {
            chatbox.classList.remove('chatbox--active');
        }
    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input'); // user input
        let text1 = textField.value;
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 } // message object
        this.messages.push(msg1);

        // http://127.0.0.1:5000/predict
        fetch($SCRIPT_ROOT + '/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors', // ei tarvii välttämättä tätä
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(r => r.json())
        .then(r => { // display the bot's answer to user
            let msg2 = { name: "Sam", message: r.answer };
            this.messages.push(msg2);
            this.updateChatText(chatbox);
            textField.value = '';

        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox);
            textField.value = '';
        });
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, ) {
            if (item.name === "Sam") 
            {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>';
            }
            else 
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>';
            }
        });

        const chatMessage = chatbox.querySelector('.chatbox__messages');
        chatMessage.innerHTML = html; // mieti vielä tää, innerHTML on riski
    }
}

const chatbox = new Chatbox();
chatbox.display();
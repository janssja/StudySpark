const chatContainer = document.getElementById('chatContainer');
const userInput = document.getElementById('userInput');

// Configureer Marked.js
marked.setOptions({
    breaks: true,        // Sta line breaks toe
    gfm: true,          // GitHub Flavored Markdown
    headerIds: false,    // Geen header IDs (voorkomt conflicten)
    mangle: false,       // Voorkom email obscuring
    sanitize: false,     // XSS wordt op een andere manier afgehandeld
    pedantic: false,     // Niet strikt in markdown parsing
    smartLists: true,    // Slimme lijstherkenning
    smartypants: true    // Mooiere quotes en dashes
});

// Voeg DOMPurify toe voor XSS beveiliging
function sanitizeHTML(html) {
    return DOMPurify.sanitize(html, {
        ALLOWED_TAGS: ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 
                      'strong', 'em', 'code', 'pre', 'blockquote', 'a', 'br', 'table', 
                      'thead', 'tbody', 'tr', 'th', 'td'],
        ALLOWED_ATTR: ['href']
    });
}

function clearChat() {
    chatContainer.innerHTML = '';
}

async function restartChat() {
    try {
        const response = await fetch('/api/restart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error('Restart failed');
        }

        // Clear the chat
        clearChat();
        
        // Add initial message
        addMessage(`# Welkom bij PXL StudySpark!

Ik ben je persoonlijke studiekeuzeadviseur. Ik help je graag bij het maken van een studiekeuze die perfect bij je past.

Zullen we beginnen?`, 'assistant');

        // Enable input
        userInput.value = '';
        userInput.disabled = false;
        userInput.focus();

    } catch (error) {
        console.error('Error restarting chat:', error);
        addMessage('Sorry, er is een fout opgetreden bij het herstarten van het gesprek.', 'assistant');
    }
}

function addMessage(message, role) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${role}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    try {
        const htmlContent = marked.parse(message);
        contentDiv.innerHTML = sanitizeHTML(htmlContent);
    } catch (e) {
        console.error('Markdown parsing error:', e);
        contentDiv.textContent = message;
    }
    
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage(message, 'user');
    userInput.value = '';
    userInput.disabled = true;

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        if (data.error) {
            throw new Error(data.error);
        }
        
        addMessage(data.response, 'assistant');
    } catch (error) {
        console.error('Error:', error);
        addMessage('Sorry, er is een fout opgetreden. Probeer het later nog eens.', 'assistant');
    } finally {
        userInput.disabled = false;
        userInput.focus();
    }
}

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});
function updateCharAndSegments(text) {
    const charCount = text.length;
    document.getElementById('charNum').innerText = charCount;
    
    const segments = Math.ceil(charCount / 160) || 1;
    const segmentBadge = document.getElementById('segmentBadge');
    segmentBadge.innerText = segments + (segments > 1 ? ' SMS parts' : ' SMS part');
    if (segments > 1) {
        segmentBadge.className = 'badge bg-warning-subtle text-warning-emphasis border border-warning-subtle';
    } else {
        segmentBadge.className = 'badge bg-light text-secondary border';
    }
}

function handleMessageInput(element) {
    const val = element.value;
    updateCharAndSegments(val);
    
    const previewText = document.getElementById('previewText');
    if (val.trim().length > 0) {
        previewText.innerText = val;
    } else {
        previewText.innerText = "Your message preview will appear here as you type...";
    }
}

function handlePhoneInput(element) {
    element.value = element.value.replace(/[^0-9]/g, '');
    const val = element.value;
    const recipientLabel = document.getElementById('previewRecipient');
    if (val.length > 0) {
        recipientLabel.innerText = '+63 ' + val;
    } else {
        recipientLabel.innerText = '+63 9XXXXXXXXX';
    }
}

function handleFormSubmit() {
    const sendBtn = document.getElementById('sendBtn');
    const btnText = document.getElementById('btnText');
    sendBtn.disabled = true;
    btnText.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Sending via Gateway...';
    document.getElementById('smsForm').submit();
}

function resetForm() {
    document.getElementById('phone_number').value = '';
    document.getElementById('message').value = '';
    document.getElementById('previewRecipient').innerText = '+63 9XXXXXXXXX';
    document.getElementById('previewText').innerText = 'Your message preview will appear here as you type...';
    updateCharAndSegments('');
}

document.addEventListener('DOMContentLoaded', function() {
    const phoneInput = document.getElementById('phone_number');
    const messageInput = document.getElementById('message');
    
    if (phoneInput && phoneInput.value) {
        handlePhoneInput(phoneInput);
    }
    if (messageInput && messageInput.value) {
        handleMessageInput(messageInput);
    }
});

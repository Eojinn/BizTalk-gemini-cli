document.addEventListener('DOMContentLoaded', () => {
    const originalTextInput = document.getElementById('original-text');
    const targetAudienceSelect = document.getElementById('target-audience');
    const convertButton = document.getElementById('convert-button');
    const convertedTextInput = document.getElementById('converted-text');
    const copyButton = document.getElementById('copy-button');
    const currentCharCount = document.getElementById('current-char-count');

    const API_BASE_URL = window.location.origin; // Dynamically get base URL

    // 1. Character count update
    originalTextInput.addEventListener('input', () => {
        currentCharCount.textContent = originalTextInput.value.length;
    });

    // 2. Convert button click handler
    convertButton.addEventListener('click', async () => {
        const originalText = originalTextInput.value;
        const target = targetAudienceSelect.value;

        if (!originalText.trim()) {
            alert('변환할 내용을 입력해주세요.');
            return;
        }

        convertButton.disabled = true;
        convertButton.textContent = '변환 중...';
        convertedTextInput.value = '변환 중입니다...';

        try {
            const response = await fetch(`${API_BASE_URL}/api/convert`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: originalText, target: target }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            convertedTextInput.value = data.converted_text;
        } catch (error) {
            console.error('Error converting text:', error);
            convertedTextInput.value = `오류 발생: ${error.message}. 다시 시도해주세요.`;
            alert('텍스트 변환 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
        } finally {
            convertButton.disabled = false;
            convertButton.textContent = '변환하기';
        }
    });

    // 3. Copy button click handler
    copyButton.addEventListener('click', async () => {
        if (!convertedTextInput.value.trim()) {
            alert('변환된 텍스트가 없습니다.');
            return;
        }

        try {
            await navigator.clipboard.writeText(convertedTextInput.value);
            alert('복사되었습니다!');
        } catch (err) {
            console.error('Failed to copy text: ', err);
            alert('텍스트 복사에 실패했습니다. 수동으로 복사해주세요.');
        }
    });
});

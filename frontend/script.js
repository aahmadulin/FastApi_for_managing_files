document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const fileList = document.getElementById('fileList');

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        try {
            const response = await fetch('http://127.0.0.1:8000/uploadfile/', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                alert('Файл успешно загружен!');
                fileInput.value = '';
                loadFiles();
            } else {
                alert('Ошибка при загрузке файла');
            }
        } catch (error) {
            console.error('Ошибка:', error);
        }
    });

    // Загрузка списка файлов
    async function loadFiles() {
        try {
            const response = await fetch('http://127.0.0.1:8000/files/');
            const files = await response.json();

            fileList.innerHTML = '';

            files.forEach(file => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <span>${file.filename} (${file.size} bytes)</span>
                    <a href="http://127.0.0.1:8000/files/${file.uid}" target="_blank">Метаданные</a>
                `;
                fileList.appendChild(li);
            });
        } catch (error) {
            console.error('Ошибка при загрузке списка файлов:', error);
        }
    }

    loadFiles();
});
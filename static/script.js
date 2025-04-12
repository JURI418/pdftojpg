// static/script.js

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("upload-form");
    const resultSection = document.getElementById("result-section");
    const downloadLink = document.getElementById("download-link");

    form.addEventListener("submit", async function (e) {
        e.preventDefault(); // 폼 제출 기본 동작 방지

        const formData = new FormData(form);

        try {
            const response = await fetch("/convert", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error("파일 변환에 실패했습니다.");
            }

            const blob = await response.blob();
            const url = URL.createObjectURL(blob);

            // 다운로드 링크 설정 및 표시
            downloadLink.href = url;
            downloadLink.download = "converted.jpg"; // 저장될 이름
            resultSection.style.display = "block";
        } catch (error) {
            alert(error.message);
        }
    });
});

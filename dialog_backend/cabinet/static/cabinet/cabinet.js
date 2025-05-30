const DIABETES_TYPES = {
    '1': '1 типа',
    '2': '2 типа',
    'mody': 'Гестационный',
    'many_types': 'Несколько типов',
}

const TREATMENT_TYPES = {
    'insulin_therapy': 'Инсулинотерапия',
    'preparations': 'Препараты',
}

const GENDER = {
    'MALE': 'Мужской',
    'FEMALE': 'Женский',
}

const INFO_MESSAGES = {
    'success_change_password': 'Пароль успешно изменен!',
    'success_edit_profile': 'Профиль успешно обновлен!',
    'filled_daily_log': 'Дневной отчет успешно заполнен!',
}

const diabetesType = document.getElementById('diabetesType')
const treatmentType = document.getElementById('treatmentType')
const gender = document.getElementById('gender')

const replaceTextToHuman = () => {
    diabetesType.textContent = DIABETES_TYPES[diabetesType.textContent];
    gender.textContent = GENDER[gender.textContent];
    treatmentType.textContent = TREATMENT_TYPES[treatmentType.textContent];
}

const getQueryParam = (param) => {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

const displayMessage = (urlParam) => {
    const toast = document.getElementById("success-toast");
    toast.textContent = INFO_MESSAGES[urlParam]

    toast.classList.remove("hidden");
    setTimeout(() => {
        toast.classList.add("opacity-100");
    }, 100);

    setTimeout(() => {
        toast.classList.remove("opacity-100");
        toast.classList.add("opacity-0");

        setTimeout(() => {
            toast.classList.add("hidden");
        }, 500);
    }, 3000);
}

const fetchDailyLogFill = async () => {
    const notifyDailyLogWindow = document.getElementById('notifyDailyLogWindow')
    const notifyDailyLogMessage = document.getElementById('notifyDailyLogMessage')

    const response = await fetch(`daily_log/filled/`)

    if (!response.ok) {
        notifyDailyLogWindow.classList.toggle('hidden')
        notifyDailyLogMessage.textContent = 'Ошибка! Дневной отчет не создан'
        return
    }

    const data = await response.json()

    if (!data['is_filled']) {
        notifyDailyLogWindow.classList.toggle('hidden')
        notifyDailyLogMessage.textContent = 'Дневной отчет не заполнен!'
    }
}

document.addEventListener('DOMContentLoaded', async (event) => {
    replaceTextToHuman();

    if (getQueryParam("success_change_password") === "true") {
        displayMessage('success_change_password');
    }
    if (getQueryParam("success_edit_profile") === "true") {
        displayMessage('success_edit_profile');
    }
    if (getQueryParam('filled_daily_log')) {
        displayMessage('filled_daily_log');
    }

    await fetchDailyLogFill();
})

const logoutForm = document.getElementById('logoutForm')
logoutForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    if (!confirm('Вы действительно хотите выйти?')) {
        return;
    }

    const form = event.target;
    const formData = new FormData(form);

    const response = await fetch(
        form.action,
        {
            method: form.method,
            body: formData,
        },
    );

    if (!response.ok) {
        alert('Ошибка выхода');
        throw new Error(`Ошибка выхода: ${response.status}`);
    }

    window.location.href = '/';

    alert('Выход успешен');
})

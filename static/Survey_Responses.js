
Chart.defaults.font.size = 18;
Chart.defaults.font.style = 'bold';
Chart.defaults.font.family = "Montserrat";
Chart.defaults.color = "#ffffff";

const ctx = document.getElementById("myChart").getContext("2d");

const labels = [
    "a",
    "b",
    "c",
    "d",
    "e",
];

const data = {
    labels,
    datasets: [
        {
            data: [40, 50, 60, 10, 30],
            label: "test",
            backgroundColor:[
                "rgba(131, 245, 226, 0.8)",
                "rgba(131, 220, 241, 0.8)",
                "rgba(131, 185, 241, 0.8)",
                "rgba(131, 170, 241, 0.8)",
                "rgba(131, 143, 241, 0.8)",
            ],
            borderWidth: 0,
            hoverBorderWidth: "3",
            hoverBorderColor: "#ffffff",
        },
    ],
};

const config = {
    type: "pie",
    data: data,
    options: {
        responsive: true,
    },
};

const myChart = new Chart(ctx, config);

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

function newChart(){
    document.getElementById('chart').insertAdjacentHTML("afterend","<div><canvas id='canvas" + cont + "'></canvas></div>");
    var can_id = "canvas" + cont;
    var ctx2 = document.getElementById(can_id).getContext('2d');
    window.can_id = new Chart(ctx2, config);

    window.can_id.update();
    //alert(config.options.id);
    configSet();
    //alert(config.options.id);
    alert(cont);
    return cont = cont + 1;
}

function configSet(){
    config.options.layout.padding.top = cont*100;
    config.options.layout.padding.bottom -= cont*100;
    //config.options.layout.padding.right -=200;
    //config.options.layout.padding.left += 200;
    config.options.id += 1;
    config.options.title.text = 'Board Number ' + config.options.id;
    //newChart();
}

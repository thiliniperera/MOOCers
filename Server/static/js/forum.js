/**
 * Created by Thilini on 10-Feb-17.
 */


var displayForumScore=function () {
$.getJSON('/json/assets/nodes.json', function (data) {

    var items = new Array(10).fill(1);
    for (i = 0; i < data.nodes.length; i++) {
        score = data.nodes[i].score

        if (score == 1) {
            rounded_score = 9
        } else {
            rounded_score = Math.floor(score * 10)
        }
        items[rounded_score] += 1
    }

    FusionCharts.ready(function () {

        var revenueChart = new FusionCharts({
            type: 'column2d',
            renderAt: 'chart-container',
            width: '550',
            height: '350',
            dataFormat: 'json',
            dataSource: {
                "chart": {
                    "caption": "Distribution of forum score",
                    "xAxisName": "Score",
                    "yAxisName": "Frequency",
                    "paletteColors": "#0075c2",
                    "bgColor": "#ffffff",
                    "borderAlpha": "20",
                    "canvasBorderAlpha": "0",
                    "usePlotGradientColor": "0",
                    "plotBorderAlpha": "10",
                    "placevaluesInside": "1",
                    "rotatevalues": "1",
                    "valueFontColor": "#ffffff",
                    "showXAxisLine": "1",
                    "xAxisLineColor": "#999999",
                    "divlineColor": "#999999",
                    "divLineIsDashed": "1",
                    "showAlternateHGridColor": "0",
                    "subcaptionFontBold": "0",
                    "subcaptionFontSize": "14"
                },
                "data": [
                        {
                    "label": "0",
                    "value": items[0]
                },
                {
                    "label": "0.1",
                    "value": items[1]
                },
                    {
                    "label": "0.2",
                    "value": items[2]
                },
                {
                    "label": "0.3",
                    "value": items[3]
                },
                    {
                    "label": "0.4",
                    "value": items[4]
                },
                {
                    "label": "0.5",
                    "value": items[5]
                },
                    {
                    "label": "0.6",
                    "value": items[6]
                },
                {
                    "label": "0.7",
                    "value": items[7]
                },
                    {
                    "label": "0.8",
                    "value": items[8]
                },
                {
                    "label": "0.9",
                    "value": items[9]
                }
                ]
            }
        }).render();
    });

});
}



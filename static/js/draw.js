(function ($, google, root) {
    google.charts.load('current', {'packages': ['corechart', 'line', 'bar']});

    root.jsonpCb = function (data) {
        console.log(data);

        // part0
        processDimensionInfo(data.dimensionInfo);
        processFeatureInfo(data.featureInfo);

        // part1
        processPart1(data.part1, data.problemCategory);

        // part2
        processPart2(data.part2List);


        google.charts.setOnLoadCallback(function () {
            // part1
            drawPart1(data.part1, data.problemCategory);

            // part2
            drawPart2(data.part2List);

            // part3
            drawPart3(data.part3);

            // part4
            drawPart4(data.part4, data.problemCategory);

            // bind print event
            bindPrint(data.part2List);
        });
    };

    function processDimensionInfo(dimensionInfo) {
        $('#part0-obsv-num').text(dimensionInfo.Number_of_observations);
        $('#part0-feat-num').text(dimensionInfo.Number_of_features);
    }

    function processFeatureInfo(featureInfo) {
        var $body = $('#part0-body');
        var html = ``;
        var tr = `<tr>`;
        for (var i = 0; i < featureInfo.length; i++) {
            var row = featureInfo[i];
            if (i > 20) {
                tr = `<tr class="hidden">`
            }
            html += tr;
            html += `
                        <td>${row.feature}</td>
                        <td>${row.type}</td>
                        <td>${row.missing_count}</td>
                        <td>${row.missing_percent}</td>
                        <td>${row.unique_count}</td>
                        <td>${row.unique_percent}</td>
                     </tr>`

        }
        html += `
            <tr>
                <td colspan="6"><button id="part-0-table-button" onclick="clickPart0TableButton()" register="1" type="button" class="btn btn-default center-block">查看全部</button></td>
            </tr>
        `;

        $body.html(html)
    }


    function processPart1(part1, category) {
        if (category === 1) {
            $('#part1-cat1').show();
        } else {
            // part1
            $('#part1-cat').show();
            if (part1.descStatSum) {
                $('#part1-desc-table tbody')
                    .html(`<tr>
                                    <td>${part1.descStatSum.count}</td>
                                    <td>${part1.descStatSum.unique}</td>
                                    <td>${part1.descStatSum.top}</td>
                                    <td>${part1.descStatSum.freq}</td>
                                </tr>`);
            }
            $('#part1-skewness').text(part1.skewness);
            $('#part1-kurtosis').text(part1.kurtosis);
        }
    }

    function processPart2(part2List) {
        $('#part2-length').text(part2List && part2List.length || 0);

        var $tabDropUl = $('#myTabDrop1-contents'),
            $tabContent = $('#myTabContent');
        var $tabDropList = [],
            $tabPanelList = [];
        for (var i = 0; i < part2List.length; i++) {
            var row = part2List[i];
            var $tabDrop =
                $(`<li>
                    <a role="tab" id="${row.feature}-tab" data-panel-id="${row.feature}">@${row.feature}</a>
                </li>`);
            var $tabPanel =
                $(`<div role="tabpanel" class="tab-pane" id="${row.feature}">
                    <h2>特征: ${row.feature} <small>缺失值: ${row.missing_data}</small></h2>

                    <h3>特征可视化</h3>
                    <div class="row">
                        <div class="col-md-12" id="${row.feature}-part_2_chart_div_3_1"></div>
                    </div>

                    <h3>描述性统计摘要信息</h3>
                    <div class="row">
                        <div class="col-md-12">
                            <table class="table">
                                <thead>
                                <tr>
                                    <th>count</th>
                                    <th>mean</th>
                                    <th>std</th>
                                    <th>25%</th>
                                    <th>50%</th>
                                    <th>75%</th>
                                    <th>max</th>
                                    <th>min</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr>
                                    <td>${row.feature_desc.descriptive_statistics_summary.count}</td>
                                    <td>${row.feature_desc.descriptive_statistics_summary.mean}</td>
                                    <td>${row.feature_desc.descriptive_statistics_summary.std}</td>
                                    <td>${row.feature_desc.descriptive_statistics_summary.b25}</td>
                                    <td>${row.feature_desc.descriptive_statistics_summary.b50}</td>
                                    <td>${row.feature_desc.descriptive_statistics_summary.b75}</td>
                                    <td>${row.feature_desc.descriptive_statistics_summary.max}</td>
                                    <td>${row.feature_desc.descriptive_statistics_summary.min}</td>
                                </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <h3>取值分布图</h3>
                    <div class="row">
                        <div class="col-md-12" id="${row.feature}-part_2_chart_div_1"></div>
                    </div>

                    <h3>偏度和峰度</h3>
                    <div class="row">
                        <div class="col-md-12">
                            <table class="table">
                                <thead>
                                <tr>
                                    <th>偏度</th>
                                    <th>峰度</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr>
                                    <td>${row.feature_desc && row.feature_desc.skewness || '-'}</td>
                                    <td>${row.feature_desc && row.feature_desc.kurtosis || '-'}</td>
                                </tr>
                                <tr>
                                    <td>偏度是描述数据分布形态的统计量，其描述的是某总体取值分布的对称性。偏度为0表示数据分布形态与正态分布的偏斜程度相同；偏度大于0表示数据分布形态与正态分布相比为正偏或右偏，即数据右端有较多的极端值；偏度小于0表示其数据分布形态与正态分布相比为负偏或左偏，即数据左端有较多的极端值。偏度的绝对值数值越大表示其分布形态的偏斜程度越大。</td>
                                    <td>峰度是描述数据取值分布形态陡缓程度的统计量。峰度为0表示该数据分布与正态分布的陡缓程度相同；峰度大于0表示该数据分布与正态分布相比较为陡峭，为尖顶峰；峰度小于0表示该数据分布与正态分布相比较为平坦，为平顶峰。峰度的绝对值数值越大表示其分布形态的陡缓程度与正态分布的差异程度越大。</td>
                                </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <h3>移动统计 <br><small>移动统计通常用于消除时间序列数据中的短期波动并突出长期趋势。</small></h3>
                    <div class="row">
                        <div class="col-md-6" id="${row.feature}-part_2_chart_div_2_1"></div>
                        <div class="col-md-6" id="${row.feature}-part_2_chart_div_2_2"></div>
                    </div>

                    <h3>分解为趋势，季节性和残差<br><small>时间序列分解：趋势，季节性和残差。时间序列数据通常包含多种潜在模式，一种有效的处理方式是将其分解为多个成分，每个成分都对应一种基础模式。</small></h3>
                    <div class="row">
                        <div class="col-md-10 col-md-offset-1" id="${row.feature}-part_2_chart_div_3_2" style="border:1px solid #000"></div>
                    </div>
                    <div class="row">
                        <div class="col-md-10 col-md-offset-1" id="${row.feature}-part_2_chart_div_3_3" style="border-left:1px solid #000;border-right: 1px solid #000"></div>
                    </div>
                    <div class="row">
                        <div class="col-md-10 col-md-offset-1" id="${row.feature}-part_2_chart_div_3_4" style="border:1px solid #000"></div>
                    </div>
                    <div class="row">
                        <div class="col-md-10 col-md-offset-1" style="padding-left: 0;">
                            <p class="text-left"><small><strong>趋势：</strong>当一个时间序列数据长期增长或者长期下降时，表示该序列有趋势。在某些场合，趋势代表着“转换方向”。例如从增长的趋势转换为下降趋势。</small></p>
                            <p class="text-left"><small><strong>季节性：</strong>当时间序列中的数据受到季节性因素（例如一年的时间或者一周的时间）的影响时，表示该序列具有季节性。季节性总是一个已知并且固定的频率。由于抗糖尿病药物的成本在年底时会有变化，导致上述抗糖尿药物的月销售额存在季节性。</small></p>
                            <p class="text-left"><small><strong>周期性：</strong>当时间序列数据存在不固定频率的上升和下降时，表示该序列有周期性 。周期波动通常至少持续两年。</small></p>
                        </div>
                    </div>
                </div>`);

            $tabDropList.push($tabDrop);
            $tabPanelList.push($tabPanel);
        }
        $tabDropUl.append($tabDropList);
        $tabContent.append($tabPanelList);
    }

    function drawPart1(part1, category) {
        if (category === 1) {
            var a = [["x", "y"]];
            var b = part1;
            var c = a.concat(b);
            var data = new google.visualization.arrayToDataTable(c);

            var options = {
                title: '',
                height: 500,
                legend: {position: 'none'},
                chart: {
                    title: '',
                    subtitle: ''
                },
                bars: 'horizontal', // Required for Material Bar Charts.
                axes: {
                    x: {
                        0: {side: 'top', label: 'Percentage'} // Top x-axis.
                    }
                },
                bar: {groupWidth: "90%"}
            };
            var chart = new google.visualization.PieChart($('#top_x_div').get(0));
            chart.draw(data, options);
        } else {
            var a = [["percentile", "value"]];
            var b = part1.histogramList;
            var c = a.concat(b);
            var data = google.visualization.arrayToDataTable(c);

            var options = {
                title: '',
                histogram: {lastBucketPercentile: 5},
                legend: 'none',
                height: 500,
                hAxis: {title: 'value',},
                vAxis: {title: 'percentile',},
            };

            var chart = new google.visualization.Histogram($('#part_1_chart_div_1').get(0));
            chart.draw(data, options);
        }
    }

    function drawPart3(part3) {
        var heatmap_data = [
            {
                z: part3.matrix,
                x: part3.featureList,
                y: part3.featureList,
                type: 'heatmap',
                // showscale: true,
            }
        ];

        var layout = {
            title: '',
            annotations: [],
            xaxis: {
                ticks: '',
                side: '',
                autosize: true,
            },
            yaxis: {
                ticks: '',
                ticksuffix: ' ',
                autosize: true,

            },
            width: 1000,
            height: 1000,
            margin: {
                l: 230,
                r: 0,
                b: 200,
                t: 20,
                pad: 4
            }
        };
        var zValues = part3.matrix;
        var xValues = part3.featureList;
        var yValues = part3.featureList;

        if (part3.featureList.length < 30) {
            for (var i = 0; i < yValues.length; i++) {
                for (var j = 0; j < xValues.length; j++) {
                    var currentValue = zValues[i][j];
                    var result = {
                        xref: 'x1',
                        yref: 'y1',
                        x: xValues[j],
                        y: yValues[i],
                        text: currentValue.toFixed(2),
                        font: {
                            family: 'Arial',
                            size: 10,
                            color: 'black'
                        },
                        showarrow: false,
                    };
                    layout.annotations.push(result);
                }
            }
        }
        Plotly.plot('heatmap_div', heatmap_data, layout);
    }

    function drawPart4(part4, category) {
        if (category === 1) {
            $('#part4-cat1').show();

            var data = google.visualization.arrayToDataTable(part4.featureTargetRel);

            var options = {
                title: '',
                hAxis: {title: '',},
                vAxis: {title: '',},
                chartArea: {top: 10},
                legend: 'none',
                height: 400,
            };

            var chart = new google.visualization.ScatterChart(document.getElementById('part_4_chart_div_1'));

            chart.draw(data, options);
        } else {
            $('#part4-cat').show();

            var a = [["features", "values", {role: "style"}]];
            var b = part4.featureTargetRel;
            var c = a.concat(b);
            var data = new google.visualization.arrayToDataTable(c);

            var options = {
                height: 800,
                chartArea: {top: 0},
                fontSize: 10,
                legend: {position: "none"},
            };

            var view = new google.visualization.DataView(data);
            view.setColumns([0, 1,
                {
                    calc: "stringify",
                    sourceColumn: 1,
                    type: "string",
                    role: "annotation"
                },
                2]);

            var chart = new google.visualization.BarChart(document.getElementById('part_4_chart_div_1'));
            // Convert the Classic options to Material options.
            // chart.draw(data, google.charts.Bar.convertOptions(options));
            chart.draw(view, options);
        }
    }

    var drawFlag = {};

    function drawPart2(part2List) {
        var $tabDropUl = $('#myTabDrop1-contents'),
            $tabContent = $('#myTabContent');

        for (var i = 0; i < part2List.length; i++) {
            (function (i) {
                var row = part2List[i];

                $(`#${row.feature}-tab`).on('click', function (e) {
                    $tabDropUl.find('li').removeClass('active');
                    $(e.target).closest('li').addClass('active');
                    $tabContent.find('.tab-pane').removeClass('active');
                    $tabContent.find('#' + row.feature).addClass('active');

                    if (!drawFlag[row.feature]) {
                        // draw
                        drawPart2Chart1(row);
                        drawPart2Chart2(row);
                        drawPart2Chart3(row);
                        drawFlag[row.feature] = true;
                    }
                });
            })(i);
        }

        $(`#${part2List[0].feature}-tab`).click();
    }

    function drawPart2Chart1(row) {
        var a = [["time", "value"]];
        var b = row.feature_desc.histogram_list || [];
        var c = a.concat(b);
        var data = google.visualization.arrayToDataTable(c);

        var options = {
            histogram: {lastBucketPercentile: 17},
            bar: {gap: 0},
            legend: 'none',
            chartArea: {width: 601},
            height: 300,
            hAxis: {title: 'time'},
        };

        var chart = new google.visualization.Histogram(document.getElementById(row.feature + '-part_2_chart_div_1'));
        chart.draw(data, options);
    }

    function drawPart2Chart2(row) {
        var a = [["point", "rolling_mean"]];
        var b = row.feature_desc.rolling_mean_list || safe;
        var c = a.concat(b);
        var data = google.visualization.arrayToDataTable(c);
        var options = {
            title: ' 移动平均值:通常用于消除时间序列数据中的短期波动并突出长期趋势',
            curveType: 'function',
            legend: {position: 'none'},
            height: 300,
        };

        var chart = new google.visualization.LineChart(document.getElementById(row.feature + '-part_2_chart_div_2_1'));
        chart.draw(data, options);

        options = {
            title: ' 移动标准差',
            curveType: 'function',
            legend: {position: 'none'},
            height: 300,
        };
        a = [["point", "rolling_std"]];
        b = row.feature_desc.rolling_std_list || [];
        c = a.concat(b);
        data = google.visualization.arrayToDataTable(c);
        chart = new google.visualization.LineChart(document.getElementById(row.feature + '-part_2_chart_div_2_2'));
        chart.draw(data, options);
    }

    function drawPart2Chart3(row) {
        var data = new google.visualization.DataTable();
        data.addColumn('number', '');
        data.addColumn('number', 'trend');

        data.addRows(row.feature_desc.trend_list || []);

        var options = {
            chart: {
                title: '',
                subtitle: ''
            },
            height: 120,
            axes: {
                x: {
                    0: {side: 'top'}
                }
            }
        };
        var chart = new google.charts.Line(document.getElementById(row.feature + '-part_2_chart_div_3_2'));
        chart.draw(data, google.charts.Line.convertOptions(options));

        data = new google.visualization.DataTable();
        data.addColumn('number', '');
        data.addColumn('number', 'seasonal');

        data.addRows(row.feature_desc.seasonal_list || []);

        chart = new google.charts.Line(document.getElementById(row.feature + '-part_2_chart_div_3_3'));
        chart.draw(data, google.charts.Line.convertOptions(options));

        data = new google.visualization.DataTable();
        data.addColumn('number', '');
        data.addColumn('number', 'resid');

        data.addRows(row.feature_desc.resid_list || []);
        chart = new google.charts.Line(document.getElementById(row.feature + '-part_2_chart_div_3_4'));
        chart.draw(data, google.charts.Line.convertOptions(options));


        data = new google.visualization.DataTable();
        data.addColumn('number', '');
        data.addColumn('number', 'observed');

        data.addRows(row.feature_desc.observed_list || []);

        options = {
            chart: {
                title: '',
                subtitle: ''
            },
            height: 400,
        };
        chart = new google.visualization.LineChart(document.getElementById(row.feature + '-part_2_chart_div_3_1'));
        chart.draw(data, google.charts.Line.convertOptions(options));
    }

    $(document).on('ready', function () {

    });

    function bindPrint(part2List) {
        $('#btn-print').on('click', function () {
            for (var i = 0; i < part2List.length; i++) {
                var row = part2List[i];
                if (!drawFlag[row.feature]) {
                    console.log('DRAW');
                    // draw
                    drawPart2Chart1(row);
                    drawPart2Chart2(row);
                    drawPart2Chart3(row);
                    drawFlag[row.feature] = true;
                }
            }
            window.print();
        })
    }
})(jQuery, google, window);



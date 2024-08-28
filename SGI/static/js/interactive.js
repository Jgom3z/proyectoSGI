!function(a, b, c, d, e, f, g) {
    "use strict";
    function h(a) {
        return f.getMessage("APEXIR_" + a)
    }
    function i(a) {
        var b = h(a)
          , c = [b].concat(Array.prototype.slice.call(arguments, 1));
        return f.formatNoEscape.apply(this, c)
    }
    function j(a) {
        return "#" + b.escapeCSS(a)
    }
    var k = "a-IRR"
      , l = k + "-dialog"
      , m = k + "-sortWidget"
      , n = m + "-button"
      , o = k + "-chart-attr-not-for-pie"
      , p = k + "-group-by-column"
      , q = k + "-add-function"
      , r = k + "-column-num"
      , s = k + "-function"
      , t = k + "-function-col"
      , u = k + "-function-num"
      , v = k + "-function-num-col"
      , w = k + "-function-row-"
      , x = k + "-pivot-column"
      , y = k + "-row-column"
      , z = k + "-col-value"
      , A = k + "-singleRow-group"
      , B = "ui-button--hot"
      , C = {
        BUTTON: {
            CANCEL: h("CANCEL"),
            DELETE: h("DELETE"),
            APPLY: h("APPLY"),
            SEND: h("SEND")
        },
        DIALOG_TITLE: {
            SELECT_COLUMNS: h("SELECT_COLUMNS"),
            FILTER: h("FILTER"),
            HIGHLIGHT: h("HIGHLIGHT"),
            SORT: h("SORT"),
            CONTROL_BREAK: h("CONTROL_BREAK"),
            COMPUTATION: h("COMPUTE"),
            AGGREGATE: h("AGGREGATE"),
            CHART: h("CHART"),
            GROUP_BY: h("GROUP_BY"),
            GROUP_BY_SORT: h("GROUP_BY_SORT"),
            PIVOT: h("PIVOT"),
            PIVOT_SORT: h("PIVOT_SORT"),
            FLASHBACK: h("FLASHBACK"),
            SAVE_REPORT: h("SAVE_REPORT"),
            RENAME_REPORT: h("RENAME_REPORT"),
            DELETE_REPORT: h("DELETE_REPORT"),
            SAVE_DEFAULT_REPORT: h("SAVE_DEFAULT_REPORT"),
            RENAME_DEFAULT_REPORT: h("RENAME_DEFAULT_REPORT"),
            DELETE_DEFAULT_REPORT: h("DELETE_DEFAULT_REPORT"),
            RESET: h("RESET"),
            DOWNLOAD: h("DOWNLOAD"),
            SUBSCRIPTION: h("SUBSCRIPTION")
        }
    };
    a.widget("apex.interactiveReport", {
        version: "5.0",
        widgetEventPrefix: "interactivereport",
        suppressUpdate: !1,
        ajaxBusy: !1,
        lastFunction: null,
        idPrefix: null,
        currentAction: null,
        currentControl: null,
        currentColumnId: null,
        lastColumnId: null,
        computationId: null,
        reportId: null,
        worksheetId: null,
        region$: null,
        dialogDrop$: null,
        tempReturnElement$: null,
        viewMode: "REPORT",
        options: {
            regionId: null,
            ajaxIdentifier: null,
            toolbar: !0,
            searchField: !0,
            columnSearch: !0,
            rowsPerPageSelect: !1,
            reportsSelect: !0,
            actionsMenu: !1,
            reportViewMode: "REPORT",
            selectColumns: !0,
            filter: !0,
            rowsPerPage: !0,
            currentRowsPerPage: 50,
            maxRowsPerPage: 1e3,
            maxRowCount: null,
            sort: !0,
            controlBreak: !0,
            highlight: !0,
            compute: !0,
            aggregate: !0,
            chart: !0,
            groupBy: !0,
            pivot: !0,
            flashback: !1,
            saveReport: !0,
            saveDefaultReport: !1,
            reset: !0,
            help: !0,
            helpLink: "",
            download: !0,
            subscription: !1,
            pagination: !0,
            saveReportCategory: !1,
            detailLink: !1,
            isControlPanelCollapsed: !1,
            fixedHeader: "NONE",
            fixedHeaderMaxHeight: null,
            pageItems: null,
            actionsMenuStructure: "IG",
            beforeRefresh: null,
            afterRefresh: null
        },
        _create: function() {
            var b = this.options.regionId
              , c = this
              , d = a(j(b), apex.gPageContext$)
              , e = a(j(b + "_ir"), apex.gPageContext$);
            0 === d.length && (d = e.wrap('<div id="' + b + '"></div>')),
            this.idPrefix = this.options.regionId,
            this.reportId = this._getElement("report_id").val(),
            this.worksheetId = this._getElement("worksheet_id").val(),
            this.viewMode = this._getElement("view_mode").val(),
            this.region$ = d,
            this.dialogDrop$ = this._getElement("dialog_js"),
            this._getElement("worksheet_region").addClass(k),
            this._initOnCreate(),
            this._on(this.region$, {
                apexrefresh: function(a) {
                    this._search(),
                    a.stopPropagation()
                }
            }),
            apex.region.create(b, {
                type: "InteractiveReport",
                refresh: function() {
                    c.refresh()
                },
                widget: function() {
                    return c.element
                }
            })
        },
        _destroy: function() {
            this._getElement("worksheet_region").removeClass(k),
            apex.region.destroy(this.options.regionId)
        },
        _setOption: function(a, b) {
            this._super(a, b)
        },
        _action: function(b, c) {
            var d = a.extend({
                widgetMod: "ACTION",
                widgetAction: b
            }, c);
            this.currentAction = b,
            this._get(d)
        },
        _aggregateClear: function(a) {
            this._action("DELETE_AGGREGATE", {
                id: a
            })
        },
        _aggregateControl: function() {
            var b = this._getDialogElement("aggregate_by").val()
              , c = a.inArray(b, ["COUNT", "COUNT_DISTINCT"]) !== -1;
            this._getDialogElement("all_columns_container").toggle(c),
            this._getDialogElement("number_columns_container").toggle(!c)
        },
        _aggregateSave: function() {
            var b, c = this._getDialogElement("aggregate_by").val(), d = this._getDialogElement("aggregation").val();
            b = a.inArray(c, ["COUNT", "COUNT_DISTINCT"]) !== -1 ? this._getDialogElement("all_columns").val() : this._getDialogElement("number_columns").val(),
            this._action("SAVE_AGGREGATE", {
                id: d,
                value: c,
                x05: b
            })
        },
        _chartClear: function() {
            this.options.reportViewMode = "REPORT",
            this._action("DELETE_CHART")
        },
        _chartControl: function() {
            a("td." + o, this._getElement("dialog_js")).toggle(!this._getDialogElement("chart_type_2").prop("checked"))
        },
        _chartSave: function() {
            this.suppressUpdate = !0,
            this._action("SAVE_CHART", {
                f01: this._utilGetFormElValues([this._getId("chart_type"), this._getId("chart_label"), this._getId("chart_value"), this._getId("aggregate_by"), this._getId("label_axis_title"), this._getId("value_axis_title"), this._getId("sort")])
            })
        },
        _chartView: function() {
            this._action("VIEW_CHART")
        },
        _columnOrder: function(a) {
            var b;
            "ASC" === a || "DESC" === a ? this._action("COLUMN_ORDER", {
                f01: this.lastColumnId,
                f02: a
            }) : (b = this._utilGetFormElAttributes(),
            this._action("SORT", {
                f01: b.ids,
                f02: b.values
            }))
        },
        _columnDisplay: function() {
            var a = [];
            this._getDialogElement("shuttle_right").find("option").each(function() {
                a.push(this.value)
            }),
            this._action("SET_COLUMNS", {
                f01: a
            })
        },
        _columnHelp: function() {
            this._controlsGet("INFO", this.currentColumnId)
        },
        _columnHide: function(a) {
            var b;
            b = a ? a : this.currentColumnId,
            this._action("HIDE", {
                id: b
            })
        },
        _columnSearchShow: function(b) {
            var c, d, e = [], f = [], g = this, h = a.parseJSON(b).row;
            for (c = 0; c < h.length; c++)
                d = "0" === h[c].C,
                d ? (e.push({
                    type: "action",
                    label: h[c].D,
                    value: h[c].R,
                    action: function() {
                        g._getElement("column_search_root").removeClass("is-active"),
                        g._getElement("column_search_current_column").val(""),
                        g._getElement("search_field").attr({
                            title: "Search",
                            placeholder: ""
                        })
                    }
                }),
                e.push({
                    type: "separator"
                })) : f.push({
                    label: h[c].D,
                    value: h[c].R
                });
            e.push({
                type: "radioGroup",
                get: function() {
                    return g._getElement("column_search_current_column").val()
                },
                set: function(a) {
                    var b, d, e = this.choices;
                    for (c = 0; c < e.length; c++)
                        if (e[c].value === a) {
                            b = i("SEARCH_COLUMN", e[c].label),
                            d = e[c].value,
                            g._getElement("column_search_root").addClass("is-active"),
                            g._getElement("column_search_current_column").val(d),
                            g._getElement("search_field").attr({
                                title: b,
                                placeholder: b
                            });
                            break
                        }
                },
                choices: f
            }),
            this.searchMenu.items = e,
            this.searchMenuCallback(),
            this.searchMenuCallback = null,
            this.searchMenu = null
        },
        _computationClear: function() {
            this._action("DELETE_COMPUTATION", {
                id: this._getDialogElement("comp_id").val()
            })
        },
        _computationSave: function() {
            var a = $f_get_emptys([this._getId("column_heading"), this._getId("computation_expr")], "error", "");
            a || (this.suppressUpdate = !0,
            this._action("SAVE_COMPUTATION", {
                id: this._getDialogElement("comp_id").val(),
                value: this._getDialogElement("column_heading").val(),
                x06: this._getDialogElement("format_mask").val(),
                x07: this._getDialogElement("computation_expr").val()
            }))
        },
        _computationShow: function(a) {
            var b;
            b = a ? a : this.computationId,
            this._controlsGet("SHOW_COMPUTATION", b),
            this.computationId = null
        },
        _controlBreakOn: function(a) {
            a && (this.currentColumnId = a),
            this._action("BREAK", {
                id: this.currentColumnId
            })
        },
        _controlBreakSave: function() {
            var a, b = [];
            for (a = 1; a < 7; a++)
                b.push(this._getId("column") + "_0" + a),
                b.push(this._getId("enable") + "_0" + a);
            this._action("SAVE_BREAK", {
                f01: b,
                f02: this._utilGetFormElValues(b)
            })
        },
        _controlBreakToggle: function(a, b) {
            this._action("BREAK_TOGGLE", {
                id: a,
                value: b
            })
        },
        _controlsFormatMask: function(b) {
            this.suppressUpdate = !0,
            this.tempReturnElement$ = a(j(b)),
            this._controlsGet("FORMAT_MASK_LOV")
        },
        _controlsGet: function(a, b) {
            this._dialogReset(),
            this.currentAction = "CONTROL",
            this.currentControl = a,
            b && (this.currentColumnId = b),
            this._get({
                widgetMod: "CONTROL",
                widgetAction: a,
                id: b
            })
        },
        _controlsNarrow: function(b) {
            this.suppressUpdate = !0,
            this.tempReturnElement$ = a(j(b)),
            this._controlsGet("NARROW", this._getDialogElement("column_name").val())
        },
        _controlsRow: function(a) {
            this._controlsGet("SHOW_DETAIL", a)
        },
        _dialogCheck: function(b, c) {
            var d = "." + m
              , e = this._dialogReset;
            b && (d = b),
            c && (e = c),
            this._on(this.document, {
                click: function(b) {
                    a(b.target).closest(d).length || e.call(this)
                }
            })
        },
        _dialogColorPicker: function(b) {
            var c = this;
            a(b).each(function() {
                var b = a(this).ColorPicker({
                    eventName: "xxx",
                    onSubmit: function(b, c, d, e) {
                        var f = a(e);
                        f.val("#" + c.toUpperCase()).trigger("change").ColorPickerHide()
                    },
                    onBeforeShow: function() {
                        a(this).ColorPickerSetColor(this.value)
                    },
                    onShow: function(b) {
                        return a(b).fadeIn("fast"),
                        !1
                    },
                    onHide: function(b) {
                        return a(b).fadeOut("fast"),
                        !1
                    }
                }).ColorPickerHide();
                c._on(b, {
                    keyup: function(a) {
                        b.ColorPickerSetColor(a.target.value)
                    },
                    blur: function() {
                        b.ColorPickerHide()
                    },
                    change: function(b) {
                        var c = b.target;
                        c.value = c.value.toUpperCase(),
                        a(j(c.id + "_preview")).css("background", c.value)
                    }
                }),
                c._on(j(this.id + "_picker"), {
                    click: function(a) {
                        b.ColorPickerShow(),
                        a.preventDefault()
                    }
                }),
                a(j(this.id + "_preview")).css("background", this.value)
            })
        },
        _dialogComp: function(a, b) {
            var c = !isNaN(b) || "." === b;
            html_ReturnToTextSelection(b + "", a, c)
        },
        _dialogCurrentOperator: function() {
            var b = this._getDialogElement("column_name")
              , c = a(b.find("option")[b.prop("selectedIndex")]).attr("class");
            return this._getDialogElement(c + "_OPT")
        },
        _dialogColumnCheck: function() {
            var b = this._dialogCurrentOperator();
            a(b).siblings().hide().end().show(),
            this._dialogOperatorCheck(b)
        },
        _dialogOpen: function(a) {
            function b(a, b, c, d, e) {
                var f, i;
                f = c ? c : C.BUTTON.APPLY,
                d && (i = B),
                g.push({
                    text: f,
                    "class": i,
                    click: function() {
                        a ? b.call(h, a) : b.call(h),
                        e && h._getElement("dialog_js").dialog("close")
                    }
                })
            }
            var c, d, e, f, g, h = this;
            switch (g = [{
                text: C.BUTTON.CANCEL,
                click: function() {
                    h._getElement("dialog_js").dialog("close")
                }
            }],
            h.currentControl) {
            case "SHOW_COLUMN":
                d = C.DIALOG_TITLE.SELECT_COLUMNS,
                b(null, h._columnDisplay, null, !0, !0);
                break;
            case "SHOW_FILTER":
                d = C.DIALOG_TITLE.FILTER,
                e = h._getDialogElement("filter_id").val(),
                e && b(e, h._filterDelete, C.BUTTON.DELETE, !1, !0),
                b(e, h._filterSave, null, !0, !1);
                break;
            case "SHOW_HIGHLIGHT":
                d = C.DIALOG_TITLE.HIGHLIGHT,
                e = h._getDialogElement("highlight_id").val(),
                e && b(e, h._highlightClear, C.BUTTON.DELETE, !1, !0),
                b(e, h._highlightSave, null, !0, !1);
                break;
            case "SHOW_ORDERING":
                d = C.DIALOG_TITLE.SORT,
                b(this, h._columnOrder, null, !0, !0);
                break;
            case "SHOW_CTRL_BREAK":
                d = C.DIALOG_TITLE.CONTROL_BREAK,
                b(null, h._controlBreakSave, null, !0, !0);
                break;
            case "SHOW_COMPUTATION":
                d = C.DIALOG_TITLE.COMPUTATION,
                e = h._getDialogElement("comp_id").val(),
                e && b(null, h._computationClear, C.BUTTON.DELETE, !1, !0),
                b(null, h._computationSave, null, !0, !1);
                break;
            case "SHOW_AGGREGATE":
                d = C.DIALOG_TITLE.AGGREGATE,
                e = h._getDialogElement("aggregation").val(),
                e && b(e, h._aggregateClear, C.BUTTON.DELETE, !1, !0),
                b(null, h._aggregateSave, null, !0, !0);
                break;
            case "SHOW_CHART":
                d = C.DIALOG_TITLE.CHART,
                e = h._getDialogElement("chart_type_hidden").val(),
                e && b(null, h._chartClear, C.BUTTON.DELETE, !1, !0),
                b(null, h._chartSave, null, !0, !1);
                break;
            case "SHOW_GROUP_BY":
                d = C.DIALOG_TITLE.GROUP_BY,
                e = h._getDialogElement("group_by_id").val(),
                e && b(null, h._groupByRemove, C.BUTTON.DELETE, !1, !0),
                b(null, h._groupBySave, null, !0, !1);
                break;
            case "SHOW_GROUP_BY_SORT":
                d = C.DIALOG_TITLE.GROUP_BY_SORT,
                b(this, h._groupBySort, null, !0, !0);
                break;
            case "SHOW_PIVOT":
                d = C.DIALOG_TITLE.PIVOT,
                e = h._getDialogElement("pivot_id").val(),
                e && b(null, h._pivotRemove, C.BUTTON.DELETE, !1, !0),
                b(null, h._pivotSave, null, !0, !1);
                break;
            case "SHOW_PIVOT_SORT":
                d = C.DIALOG_TITLE.PIVOT_SORT,
                b(this, h._pivotSort, null, !0, !0);
                break;
            case "SHOW_FLASHBACK":
                d = C.DIALOG_TITLE.FLASHBACK,
                e = h._getDialogElement("flashback_time").val(),
                e && b(null, h._flashbackClear, C.BUTTON.DELETE, !1, !0),
                b(null, h._flashbackSave, null, !0, !1);
                break;
            case "SAVE_REPORT":
                d = C.DIALOG_TITLE.SAVE_REPORT,
                b(null, h._save, null, !0, !1);
                break;
            case "SHOW_RENAME":
                d = C.DIALOG_TITLE.RENAME_REPORT,
                b(h.reportId, h._save, null, !0, !1);
                break;
            case "SHOW_DELETE":
                d = C.DIALOG_TITLE.DELETE_REPORT,
                b(null, h._remove, null, !0, !0);
                break;
            case "SHOW_SAVE_DEFAULT":
                d = C.DIALOG_TITLE.SAVE_DEFAULT_REPORT,
                b(null, h._saveDefault, null, !0, !1);
                break;
            case "SHOW_RENAME_DEFAULT":
                d = C.DIALOG_TITLE.RENAME_DEFAULT_REPORT,
                b("RENAME_DEFAULT", h._saveDefault, null, !0, !1);
                break;
            case "SHOW_DELETE_DEFAULT":
                d = C.DIALOG_TITLE.DELETE_DEFAULT_REPORT,
                b("DELETE_DEFAULT", h._remove, null, !0, !0);
                break;
            case "SHOW_RESET":
                d = C.DIALOG_TITLE.RESET,
                b(null, h._reset, null, !0, !0);
                break;
            case "SHOW_DOWNLOAD":
                d = C.DIALOG_TITLE.DOWNLOAD;
                break;
            case "SHOW_NOTIFY":
                d = C.DIALOG_TITLE.SUBSCRIPTION,
                e = h._getDialogElement("notify_id").val(),
                f = h._getDialogElement("email_not_configured").text(),
                e && b(null, h._notifyClear, C.BUTTON.DELETE, !1, !0),
                f || b(null, h._notifySave, null, !0, !1)
            }
            c = this._getElement("dialog_js").dialog({
                modal: !0,
                dialogClass: l,
                width: "auto",
                height: "auto",
                minWidth: "360",
                title: d,
                buttons: g,
                position: {
                    my: "left+10 top+10",
                    at: "left top",
                    of: this._getElement("content")
                },
                close: function() {
                    h._off(c),
                    c.dialog("destroy")
                }
            }),
            a && a.call()
        },
        _dialogColumnHandlers: function() {
            this._on(this._getDialogElement("column_name"), {
                change: function() {
                    this._dialogColumnCheck()
                }
            }),
            this._on(this._getElement("dialog_js"), {
                "change select.a-IRR-operator": function(b) {
                    this._dialogOperatorCheck(a(b.target))
                },
                "click button.a-Button--menu": function(b) {
                    var c = a(b.currentTarget).data("picker-for");
                    this._controlsNarrow(c)
                }
            })
        },
        _dialogOperatorCheck: function(b) {
            var c, d = [], e = b.val(), f = b.data("column-type"), g = ["is in the last", "is not in the last", "is in the next", "is not in the next"];
            d[0] = $x(this._getId("expression")).parentNode,
            d[1] = $x(this._getId("expression2")).parentNode,
            d[2] = $x(this._getId("expression3")).parentNode,
            d[3] = $x(this._getId("between_from")).parentNode,
            d[4] = $x(this._getId("between_to")).parentNode,
            $x_Show_Hide(this._getId("expression_icon_link"), d),
            "is null" === e || "is not null" === e ? this._getDialogElement("expression_label").hide() : (this._getDialogElement("expression_label").show(),
            "DATE" === f && a.inArray(e, g) === -1 ? ($x_Show(d[3]),
            c = this._getDialogElement("column_name").find(":selected").data("format-mask"),
            this._setDateFieldFormatMask(this._getDialogElement("between_from"), c),
            "between" === e && ($x_Show(d[4]),
            this._setDateFieldFormatMask(this._getDialogElement("between_to"), c))) : ($x_Show(d[0]),
            "between" === e && $x_Show(d[1]),
            a.inArray(e, g) > -1 && $x_Show_Hide(d[2], this._getId("expression_icon_link"))))
        },
        _dialogReset: function() {
            this.suppressUpdate || (this.currentColumnId = null,
            this.computationId = null,
            this._off(this.document, "click"))
        },
        _dialogUtilExpType: function() {
            var a = {};
            return a.col = $x(this._getId("column_name")),
            a.col_type = a.col.options[a.col.selectedIndex].className,
            a.col_opt = $x(this._getId(a.col_type + "_OPT")),
            a.col_opt_val = $v(a.col_opt),
            "DATE" === a.col_type && "is in the last" !== a.col_opt_val && "is not in the last" !== a.col_opt_val && "is in the next" !== a.col_opt_val && "is not in the next" !== a.col_opt_val ? a.form_items = [this._getId("between_from"), this._getId("between_to")] : a.form_items = [this._getId("expression"), this._getId("expression2")],
            a
        },
        _dialogValidate: function() {
            var a = []
              , b = this._dialogUtilExpType();
            switch (!0) {
            case "between" === b.col_opt_val:
                a = [b.form_items[0], b.form_items[1]];
                break;
            case "is null" === b.col_opt_val || "is not null" === b.col_opt_val:
                a = [];
                break;
            case "is in the last" === b.col_opt_val || "is not in the last" === b.col_opt_val || "is in the next" === b.col_opt_val || "is not in the next" === b.col_opt_val:
                a = [b.form_items[0], this._getId("expression3")];
                break;
            default:
                a = [b.form_items[0]]
            }
            return !$f_get_emptys(a, "error", "") && b
        },
        _emailSend: function() {
            var a, b = [this._getId("email_to")], c = $f_get_emptys(b, "error", "");
            c || (a = [this._getId("email_to"), this._getId("email_cc"), this._getId("email_bcc"), this._getId("email_subject"), this._getId("email_body")],
            this._action("SEND_EMAIL", {
                f01: a,
                f02: this._utilGetFormElValues(a)
            }),
            this._getElement("dialog_js").dialog("close"))
        },
        _emailShow: function() {
            var a, b = this, c = this._getElement("dialog_js"), d = this._getDialogElement("email"), e = this._getDialogElement("email_button");
            d.show(),
            e.show(),
            e.is(":visible") && (a = [{
                text: C.BUTTON.CANCEL,
                click: function() {
                    c.dialog("close")
                }
            }, {
                text: C.BUTTON.SEND,
                "class": B,
                click: function() {
                    b._emailSend()
                }
            }],
            c.dialog("option", "buttons", a))
        },
        _filterDelete: function(a) {
            this._action("FILTER_DELETE", {
                id: a
            })
        },
        _filterSave: function(a) {
            var b, c, d = "ADD", e = this._getId("filter_type");
            if (a ? (this.currentColumnId = a,
            d = "UPDATE") : a = this._getDialogElement("column_name").val(),
            "COLUMN" === $v(e)) {
                if (b = this._dialogValidate(),
                !b)
                    return;
                c = [e, b.col.id, b.col_opt.id, b.form_items[0], b.form_items[1], this._getId("expression3")]
            } else
                c = [e, this._getId("filter_expr"), this._getId("filter_name")];
            this.suppressUpdate = !0,
            this._action("FILTER", {
                widgetActionMod: d,
                f01: this._utilGetFormElValues(c),
                id: a
            })
        },
        _flashbackSave: function() {
            this.suppressUpdate = !0,
            this._action("FLASHBACK_SET", {
                value: this._getDialogElement("flashback_time").val()
            })
        },
        _filterToggle: function(a, b) {
            this._action("FILTER_TOGGLE", {
                id: a,
                value: b
            })
        },
        _flashbackClear: function() {
            this._action("FLASHBACK_CLEAR")
        },
        _flashbackToggle: function() {
            this._action("FLASHBACK_TOGGLE")
        },
        _functionControl: function(b) {
            var c, d, e, f = ["SUM", "AVG", "MAX", "MIN", "MEDIAN", "RATIO_TO_REPORT_SUM"];
            b && (c = b.id,
            d = c.substr(c.length - 2),
            e = a.inArray(a(b).val(), f) !== -1,
            this._getDialogElement("number_columns_container_" + d).toggle(e),
            this._getDialogElement("all_columns_container_" + d).toggle(!e))
        },
        _get: function(b) {
            function c(b) {
                var c, d, e, f, h, i;
                if ("CONTROL" === j.currentAction) {
                    if ("SORT_WIDGET" === j.currentControl)
                        j._sortWidgetShow(b);
                    else if ("INFO" === j.currentControl)
                        j._helpWidgetShow(b);
                    else if ("NARROW" === j.currentControl)
                        c = j._inlinePicker("NARROW", b);
                    else if ("FORMAT_MASK_LOV" === j.currentControl)
                        c = j._inlinePicker("FORMAT_MASK_LOV", b);
                    else if ("SEARCH_COLUMN" === j.currentControl)
                        j._columnSearchShow(b);
                    else if ("SHOW_DETAIL" === j.currentControl)
                        j._singleRowViewShow(b);
                    else {
                        switch (j.currentControl) {
                        case "SHOW_FILTER":
                            e = function() {
                                j._dialogColumnCheck(),
                                j._dialogColumnHandlers(),
                                j._on(j._getDialogElement("filter_type"), {
                                    "click input": function(a) {
                                        var b = "COLUMN" === a.target.value;
                                        j._getDialogElement("column_filter").toggle(b),
                                        j._getDialogElement("row_filter").toggle(!b)
                                    }
                                }),
                                j._on(j._getDialogElement("filter_expr_clear"), {
                                    click: function(a) {
                                        j._getDialogElement("filter_expr").val(""),
                                        a.preventDefault()
                                    }
                                }),
                                j._on(j._getDialogElement("row_filter_columns"), {
                                    "click tr.a-IRR-row-filter-column": function(b) {
                                        var c = a(b.currentTarget).data("column-id");
                                        j._dialogComp(j._getId("filter_expr"), c),
                                        b.preventDefault()
                                    }
                                }),
                                j._on(j._getDialogElement("row_filter_operators"), {
                                    "click tr.a-IRR-row-filter-operator": function(b) {
                                        var c = a(b.currentTarget).data("operator");
                                        j._dialogComp(j._getId("filter_expr"), c),
                                        b.preventDefault()
                                    }
                                })
                            }
                            ;
                            break;
                        case "SHOW_HIGHLIGHT":
                            e = function() {
                                j._dialogColumnCheck(),
                                j._dialogColumnHandlers(),
                                j._dialogColorPicker(j._getIdSelector("bg_color") + "," + j._getIdSelector("font_color"))
                            }
                            ;
                            break;
                        case "SHOW_CHART":
                            e = function() {
                                j._chartControl(),
                                j._on(j._getDialogElement("chart_type"), {
                                    "click input": function() {
                                        j._chartControl()
                                    }
                                })
                            }
                            ;
                            break;
                        case "SHOW_COMPUTATION":
                            e = function() {
                                j._on(j._getDialogElement("comp_id"), {
                                    change: function(b) {
                                        j._computationShow(a(b.currentTarget).val())
                                    }
                                }),
                                j._on(j._getDialogElement("format_mask_picker"), {
                                    click: function(a) {
                                        j._controlsFormatMask(j._getId("format_mask")),
                                        a.preventDefault()
                                    }
                                }),
                                j._on(j._getDialogElement("computation_expr_clear"), {
                                    click: function(a) {
                                        j._getDialogElement("computation_expr").val(""),
                                        a.preventDefault()
                                    }
                                }),
                                j._on(j._getDialogElement("computation_columns"), {
                                    "click tr.a-IRR-computation-column": function(b) {
                                        var c = a(b.currentTarget).data("column-id");
                                        j._dialogComp(j._getId("computation_expr"), c),
                                        b.preventDefault()
                                    }
                                }),
                                j._on(j._getDialogElement("computation_keypad"), {
                                    "click td.a-IRR-key": function(b) {
                                        var c = a(b.currentTarget).data("key");
                                        j._dialogComp(j._getId("computation_expr"), c),
                                        b.preventDefault()
                                    }
                                }),
                                j._on(j._getDialogElement("computation_functions"), {
                                    "click tr.a-IRR-computation-function": function(b) {
                                        var c = a(b.currentTarget).data("function");
                                        j._dialogComp(j._getId("computation_expr"), c),
                                        b.preventDefault()
                                    }
                                })
                            }
                            ;
                            break;
                        case "SHOW_COLUMN":
                            e = function() {
                                if (j.g_Shuttlep_v01 = null,
                                !a)
                                    var a = [];
                                a[2] = $x(j._getId("shuttle_left")),
                                a[1] = $x(j._getId("shuttle_right")),
                                window.g_Shuttlep_v01 = new dhtml_ShuttleObject(a[2],a[1])
                            }
                            ;
                            break;
                        case "SAVE_REPORT":
                            e = function() {
                                j._on(j._getDialogElement("save_option"), {
                                    change: function(a) {
                                        j._controlsGet(a.target.value)
                                    }
                                }),
                                j.options.saveReportCategory && j._on(j._getDialogElement("report_category"), {
                                    change: function(a) {
                                        j._saveCategoryCheck(a.target)
                                    }
                                })
                            }
                            ;
                            break;
                        case "SHOW_SAVE_DEFAULT":
                        case "SHOW_RENAME_DEFAULT":
                            e = function() {
                                j._on(j._getDialogElement("default_type"), {
                                    "click input": function(a) {
                                        this._saveDefaultTypeCheck(a.target.value)
                                    }
                                }),
                                j._saveDefaultTypeCheck($v(j._getId("default_type")))
                            }
                            ;
                            break;
                        case "SHOW_AGGREGATE":
                            e = function() {
                                j._on(j._getDialogElement("aggregation"), {
                                    change: function(b) {
                                        this._controlsGet("SHOW_AGGREGATE", a(b.currentTarget).val())
                                    }
                                }),
                                j._on(j._getDialogElement("aggregate_by"), {
                                    change: function() {
                                        this._aggregateControl()
                                    }
                                })
                            }
                            ;
                            break;
                        case "SHOW_DOWNLOAD":
                            e = function() {
                                j._on(j._getDialogElement("download_EMAIL"), {
                                    click: function(a) {
                                        j._emailShow(),
                                        a.preventDefault()
                                    }
                                })
                            }
                            ;
                            break;
                        case "SHOW_GROUP_BY":
                            e = function() {
                                j._on(j._getDialogElement("add_column"), {
                                    click: function(a) {
                                        this._utilAddMoreColumn(this._groupByMaxValue, p),
                                        a.preventDefault()
                                    }
                                }),
                                j._on(j._getDialogElement("group_by_functions"), {
                                    "change select.a-IRR-function": function(a) {
                                        this._functionControl(a.target)
                                    },
                                    "click a.a-IRR-format-mask-picker": function(b) {
                                        j._controlsFormatMask(a(b.currentTarget).data("picker-for")),
                                        b.preventDefault()
                                    }
                                }),
                                j._on(j._getDialogElement("add_function"), {
                                    click: function(a) {
                                        this._utilAddMoreFunction(this._groupByMaxValue),
                                        a.preventDefault()
                                    }
                                })
                            }
                            ;
                            break;
                        case "SHOW_PIVOT":
                            e = function() {
                                j._on(j._getDialogElement("add_pivot_column"), {
                                    click: function(a) {
                                        this._utilAddMoreColumn(this._pivotMaxValue, x),
                                        a.preventDefault()
                                    }
                                }),
                                j._on(j._getDialogElement("add_row_column"), {
                                    click: function(a) {
                                        this._utilAddMoreColumn(this._pivotMaxValue, y),
                                        a.preventDefault()
                                    }
                                }),
                                j._on(j._getDialogElement("pivot_functions"), {
                                    "change select.a-IRR-function": function(a) {
                                        this._functionControl(a.target)
                                    },
                                    "click a.a-IRR-format-mask-picker": function(b) {
                                        j._controlsFormatMask(a(b.currentTarget).data("picker-for")),
                                        b.preventDefault()
                                    }
                                }),
                                j._on(j._getDialogElement("add_function"), {
                                    click: function(a) {
                                        this._utilAddMoreFunction(this._pivotMaxValue),
                                        a.preventDefault()
                                    }
                                })
                            }
                        }
                        j._getElement("dialog_js").html(b),
                        j._dialogOpen(e)
                    }
                    c === g && (c = a(":input:visible", j._getElement("dialog_js"))),
                    c.length > 0 && c[0].focus()
                } else
                    j.suppressUpdate ? (d = ["SAVE_NOTIFY", "SAVE_COMPUTATION", "FLASHBACK_SET", "SAVE_HIGHLIGHT", "FILTER", "GROUP_BY_SAVE", "SAVE_PIVOT", "SAVE_CHART"],
                    a.inArray(j.currentAction, d) > -1 && (j.lastFunction = function() {
                        j._validAction(b)
                    }
                    ),
                    j.ajaxBusy = !1,
                    j.suppressUpdate = !1,
                    j.currentAction = null) : (f = a($u_js_temp_drop()),
                    f.html(b),
                    h = f.find(j._getIdSelector("toolbar_controls")),
                    i = f.find(j._getIdSelector("content")),
                    j._getElement("toolbar_controls", j.element).replaceWith(h),
                    j._getElement("content", j.element).replaceWith(i),
                    j.options.currentRowsPerPage = 1 * j._getElement("row_select").val(),
                    j.viewMode = j._getElement("view_mode").val(),
                    j._initToolbar(),
                    j._initControlPanel(),
                    j.currentAction = null,
                    j.currentControl = null,
                    j.reportId = j._getElement("report_id").val(),
                    j._singleRowViewHide(),
                    j._getElement("full_view").show(),
                    f.remove(),
                    j._initFixedHeader(!0),
                    a(":focus").length || (c = j.element.find(":focusable"),
                    c.length > 0 && c[0].focus()))
            }
            function e() {
                j.lastFunction && (j.lastFunction(),
                j.lastFunction = !1),
                j.ajaxBusy = !1,
                "SEARCH_COLUMN" === j.currentControl && j.searchMenuCallback && (j.searchMenuCallback(!1),
                j.searchMenuCallback = null,
                j.searchMenu = null)
            }
            var f, h, i, j = this, k = !1;
            "INFO" !== b.widgetAction && this._sortWidgetHide(),
            b.widgetMod && !this.suppressUpdate && (a.inArray(b.widgetMod, ["ACTION", "PULL"]) !== -1 ? k = !0 : "CONTROL" === b.widgetMod && b.widgetAction && "SHOW_DETAIL" === b.widgetAction && (k = !0)),
            f = a.extend({
                p_widget_name: "worksheet",
                p_widget_mod: b.widgetMod,
                p_widget_action: b.widgetAction,
                p_widget_action_mod: b.widgetActionMod,
                p_widget_num_return: j.options.currentRowsPerPage,
                x01: j.worksheetId,
                x02: j.reportId,
                x03: b.id,
                x04: b.value,
                pageItems: this.options.pageItems
            }, b),
            delete f.widgetMod,
            delete f.widgetAction,
            delete f.widgetActionMod,
            delete f.id,
            delete f.value,
            "RESET" !== f.p_widget_action && "REPORT_CHANGED" !== f.p_widget_action || delete f.p_widget_num_return,
            f.p_widget_action_mod || delete f.p_widget_action_mod,
            h = {
                dataType: "html",
                refreshObject: k ? this.region$ : null,
                loadingIndicator: j._getElement("worksheet_region"),
                loadingIndicatorPosition: "centered",
                success: c,
                complete: e
            },
            i = d.plugin(this.options.ajaxIdentifier, f, h),
            i || (this.ajaxBusy = !1)
        },
        _getId: function(a) {
            return this.idPrefix + "_" + a
        },
        _getIdSelector: function(a) {
            return j(this._getId(a))
        },
        _getElement: function(b, c) {
            var d;
            return d = c ? c : "dialog_js" === b || /^sort_widget.*$/.test(b) ? apex.gPageContext$ : this.element,
            a(this._getIdSelector(b), d)
        },
        _getDialogElement: function(a) {
            return this._getElement(a, this._getElement("dialog_js"))
        },
        _groupByMaxValue: 8,
        _groupByRemove: function() {
            this._action("GROUP_BY_REMOVE")
        },
        _groupBySave: function() {
            var a = this._utilGetFormElAttributes();
            this.suppressUpdate = !0,
            this._action("GROUP_BY_SAVE", {
                f01: a.ids,
                f02: a.values
            })
        },
        _groupBySort: function(a) {
            var b, c = this._getDialogElement("group_by_id").val();
            "ASC" === a || "DESC" === a ? (this.lastColumnId = a.id,
            this._action("GROUP_BY_COLUMN_SORT", {
                id: c,
                f01: this.lastColumnId,
                f02: a
            })) : (b = this._utilGetFormElAttributes(),
            this._action("GROUP_BY_SORT", {
                id: c,
                f01: b.ids,
                f02: b.values
            }))
        },
        _groupByView: function() {
            this._action("VIEW_GROUP_BY")
        },
        _helpWidgetShow: function(a) {
            this._getElement("sort_widget_help").html(a).show(),
            this._getElement("sort_widget_action_help").find("button.a-IRR-sortWidget-button").addClass("is-active"),
            this.lastColumnId = this.currentColumnId,
            this._dialogCheck(null, this._sortWidgetHide)
        },
        _highlightClear: function(a) {
            var b;
            b = a ? a : $x("HIGHLIGHT_ID").value,
            this._action("CLEAR_HIGHLIGHT", {
                id: b
            })
        },
        _highlightSave: function() {
            var a, b = this._dialogValidate();
            b && (this.suppressUpdate = !0,
            a = this._utilGetFormElAttributes(),
            this._action("SAVE_HIGHLIGHT", {
                f01: a.ids,
                f02: a.values
            }),
            b = null)
        },
        _highlightToggle: function(a, b) {
            this._action("TOGGLE_HIGHLIGHT", {
                id: a,
                value: b
            })
        },
        _initControlPanel: function() {
            function b() {
                d.options.isControlPanelCollapsed && (d.options.isControlPanelCollapsed = !1,
                d.suppressUpdate = !0,
                d._action("CONTROL_MIN", {
                    value: "N"
                })),
                d._getElement("control_panel_summary").hide()
            }
            function c() {
                d.options.isControlPanelCollapsed || (d.options.isControlPanelCollapsed = !0,
                d.suppressUpdate = !0,
                d._action("CONTROL_MIN", {
                    value: "Y"
                })),
                d._getElement("control_panel_summary").show()
            }
            var d = this;
            this._on(this._getElement("control_panel"), {
                "click a.a-IRR-controlsLabel": function(b) {
                    var c = a(b.currentTarget)
                      , e = c.data("setting");
                    switch (e) {
                    case "filter":
                        this._controlsGet("SHOW_FILTER", c.data("filter-id"));
                        break;
                    case "report":
                        this._controlsGet("SHOW_RENAME");
                        break;
                    case "report-default":
                        this._controlsGet("SHOW_RENAME_DEFAULT");
                        break;
                    case "highlight":
                        this._controlsGet("SHOW_HIGHLIGHT", c.data("highlight-id"));
                        break;
                    case "break":
                        this._controlsGet("SHOW_CTRL_BREAK");
                        break;
                    case "chart":
                        this._controlsGet("SHOW_CHART");
                        break;
                    case "group_by":
                        this._controlsGet("SHOW_GROUP_BY");
                        break;
                    case "pivot":
                        this._controlsGet("SHOW_PIVOT");
                        break;
                    case "flashback":
                        d._controlsGet("SHOW_FLASHBACK")
                    }
                    b.preventDefault()
                },
                "click a.a-IRR-reportSummary-label": function(b) {
                    var c = a(b.currentTarget)
                      , e = c.data("setting");
                    switch (e) {
                    case "filter":
                        this._controlsGet("SHOW_FILTER", c.data("filter-id"));
                        break;
                    case "report":
                        this._controlsGet("SHOW_RENAME");
                        break;
                    case "report-default":
                        this._controlsGet("SHOW_RENAME_DEFAULT");
                        break;
                    case "highlight":
                        this._controlsGet("SHOW_HIGHLIGHT", c.data("highlight-id"));
                        break;
                    case "break":
                        this._controlsGet("SHOW_CTRL_BREAK");
                        break;
                    case "chart":
                        this._controlsGet("SHOW_CHART");
                        break;
                    case "group-by":
                        this._controlsGet("SHOW_GROUP_BY");
                        break;
                    case "pivot":
                        this._controlsGet("SHOW_PIVOT");
                        break;
                    case "flashback":
                        d._controlsGet("SHOW_FLASHBACK");
                        break;
                    default:
                        d._getElement("control_panel").collapsible("expand")
                    }
                    b.preventDefault()
                },
                "click input.a-IRR-controlsCheckbox": function(b) {
                    var c = a(b.target)
                      , d = c.prop("checked") ? "Y" : "N"
                      , e = c.data("setting");
                    switch (e) {
                    case "break":
                        this._controlBreakToggle(c.data("break-column"), d);
                        break;
                    case "filter":
                        this._filterToggle(c.data("filter-id"), d);
                        break;
                    case "highlight":
                        this._highlightToggle(c.data("highlight-id"), d);
                        break;
                    case "flashback":
                        this._flashbackToggle()
                    }
                },
                "click button.a-IRR-button--remove": function(b) {
                    var c = a(b.currentTarget)
                      , d = c.data("setting");
                    switch (d) {
                    case "break":
                        this._controlBreakOn(c.data("break-column"));
                        break;
                    case "breaks":
                        break;
                    case "filter":
                        this._filterDelete(c.data("filter-id"));
                        break;
                    case "filters":
                        break;
                    case "report":
                        this._controlsGet("SHOW_DELETE");
                        break;
                    case "report-default":
                        this._controlsGet("SHOW_DELETE_DEFAULT");
                        break;
                    case "highlight":
                        this._highlightClear(c.data("highlight-id"));
                        break;
                    case "highlights":
                        break;
                    case "flashback":
                        this._flashbackClear();
                        break;
                    case "chart":
                        this._chartClear();
                        break;
                    case "group-by":
                        this._groupByRemove();
                        break;
                    case "pivot":
                        this._pivotRemove()
                    }
                    b.preventDefault()
                }
            }),
            this._getElement("control_panel").collapsible({
                content: "div.a-MediaBlock-content",
                collapsed: d.options.isControlPanelCollapsed,
                collapse: c,
                expand: b
            })
        },
        _initFixedHeader: function(b) {
            var c, d = this.options;
            if (!$x("pScreenReaderMode") && ("PAGE" === d.fixedHeader || "REGION" === d.fixedHeader) && 0 === a(".a-IRR-header--group", this.element).length) {
                switch (this.viewMode) {
                case "REPORT":
                    "REPORT" === d.reportViewMode && (c = "a-IRR-reportView");
                    break;
                case "GROUP_BY":
                    c = "a-IRR-groupByView"
                }
                if (c) {
                    if (0 === a(this.element).find(".a-IRR-iconViewTable").length)
                        switch (d.fixedHeader) {
                        case "PAGE":
                            a("." + c, this.element).setTableHeadersAsFixed(),
                            a(".js-stickyTableHeader", this.element).stickyWidget({
                                toggleWidth: !0,
                                stickToEnd: !0
                            });
                            break;
                        case "REGION":
                            a("." + c, this.element).setTableHeadersAsFixed({
                                maxHeight: d.fixedHeaderMaxHeight
                            })
                        }
                    b && a(window).trigger("apexwindowresized")
                }
            }
        },
        _initMenus: function() {
            function a(a, b) {
                var c;
                for (c = 0; c < a.length; c++)
                    if (a[c].id === b)
                        return a[c]
            }
            var b, c = this, d = this.options, f = [1, 5, 10, 15, 20, 25, 50, 100, 1e3];
            b = "IG" === d.actionsMenuStructure ? {
                items: [{
                    id: "irColumn",
                    type: "action",
                    label: h("COLUMNS"),
                    hide: !0,
                    icon: "icon-irr-select-cols",
                    action: function() {
                        c._controlsGet("SHOW_COLUMN", "COLUMN")
                    }
                }, {
                    type: "separator"
                }, {
                    id: "irFilter",
                    type: "action",
                    label: h("FILTER"),
                    hide: !0,
                    icon: "icon-irr-filter",
                    action: function() {
                        c._controlsGet("SHOW_FILTER")
                    }
                }, {
                    id: "irData",
                    type: "subMenu",
                    label: h("DATA"),
                    hide: !1,
                    icon: "icon-ig-data",
                    menu: {
                        items: [{
                            id: "irOrdering",
                            type: "action",
                            label: h("SORT"),
                            hide: !0,
                            icon: "icon-irr-sort",
                            action: function() {
                                c._controlsGet("SHOW_ORDERING")
                            }
                        }, {
                            id: "irGroupBySort",
                            type: "action",
                            label: h("GROUP_BY_SORT"),
                            hide: !0,
                            icon: "icon-irr-sort",
                            action: function() {
                                c._controlsGet("SHOW_GROUP_BY_SORT")
                            }
                        }, {
                            id: "irPivotSort",
                            type: "action",
                            label: h("PIVOT_SORT"),
                            hide: !0,
                            icon: "icon-irr-sort",
                            action: function() {
                                c._controlsGet("SHOW_PIVOT_SORT")
                            }
                        }, {
                            id: "irAggregate",
                            type: "action",
                            label: h("AGGREGATE"),
                            hide: !0,
                            icon: "icon-irr-aggregate",
                            action: function() {
                                c._controlsGet("SHOW_AGGREGATE")
                            }
                        }, {
                            id: "irCompute",
                            type: "action",
                            label: h("COMPUTE"),
                            hide: !0,
                            icon: "icon-irr-compute",
                            action: function() {
                                c._computationShow()
                            }
                        }, {
                            id: "irFlashback",
                            type: "action",
                            label: h("FLASHBACK"),
                            hide: !0,
                            icon: "icon-irr-flashback",
                            action: function() {
                                c._controlsGet("SHOW_FLASHBACK")
                            }
                        }]
                    }
                }, {
                    id: "irFormat",
                    type: "subMenu",
                    label: h("FORMAT"),
                    hide: !1,
                    icon: "icon-irr-format",
                    menu: {
                        items: [{
                            id: "irCtrlBreak",
                            type: "action",
                            label: h("CONTROL_BREAK"),
                            hide: !0,
                            icon: "icon-irr-control-break",
                            action: function() {
                                c._controlsGet("SHOW_CTRL_BREAK")
                            }
                        }, {
                            id: "irHighlight",
                            type: "action",
                            label: h("HIGHLIGHT"),
                            hide: !0,
                            icon: "icon-irr-highlight",
                            action: function() {
                                c._controlsGet("SHOW_HIGHLIGHT")
                            }
                        }, {
                            id: "irRowsPerPage",
                            type: "subMenu",
                            label: h("ROWS_PER_PAGE"),
                            hide: !0,
                            icon: "icon-irr-rows",
                            menu: {
                                items: [{
                                    type: "radioGroup",
                                    set: function(a) {
                                        c.options.currentRowsPerPage = 1 * a,
                                        c._search("SEARCH")
                                    },
                                    get: function() {
                                        return c.options.currentRowsPerPage
                                    },
                                    choices: []
                                }]
                            }
                        }]
                    }
                }, {
                    type: "separator"
                }, {
                    id: "irChart",
                    type: "action",
                    label: h("CHART"),
                    hide: !0,
                    icon: "icon-irr-chart",
                    action: function() {
                        c._controlsGet("SHOW_CHART")
                    }
                }, {
                    id: "irGroupBy",
                    type: "action",
                    label: h("GROUP_BY"),
                    hide: !0,
                    icon: "icon-irr-group-by",
                    action: function() {
                        c._controlsGet("SHOW_GROUP_BY")
                    }
                }, {
                    id: "irPivot",
                    type: "action",
                    label: h("PIVOT"),
                    hide: !0,
                    icon: "icon-irr-pivot",
                    action: function() {
                        c._controlsGet("SHOW_PIVOT")
                    }
                }, {
                    type: "separator"
                }, {
                    id: "irReport",
                    type: "subMenu",
                    label: h("REPORT"),
                    hide: !1,
                    icon: "icon-irr-saved-report",
                    menu: {
                        items: [{
                            id: "irSaveReport",
                            type: "action",
                            label: h("SAVE_REPORT"),
                            hide: !0,
                            icon: "icon-ig-save",
                            action: function() {
                                c._controlsGet("SAVE_REPORT")
                            }
                        }, {
                            id: "irSaveDefault",
                            type: "action",
                            label: h("SAVE_REPORT_DEFAULT"),
                            hide: !0,
                            icon: "icon-ig-save",
                            action: function() {
                                c._controlsGet("SHOW_SAVE_DEFAULT")
                            }
                        }, {
                            type: "separator"
                        }, {
                            id: "irReset",
                            type: "action",
                            label: h("RESET"),
                            hide: !0,
                            icon: "icon-irr-reset",
                            action: function() {
                                c._controlsGet("SHOW_RESET")
                            }
                        }]
                    }
                }, {
                    type: "separator"
                }, {
                    id: "irDownload",
                    type: "action",
                    label: h("DOWNLOAD"),
                    hide: !0,
                    icon: "icon-irr-download",
                    action: function() {
                        c._controlsGet("SHOW_DOWNLOAD")
                    }
                }, {
                    id: "irNotify",
                    type: "action",
                    label: h("SUBSCRIPTION"),
                    hide: !0,
                    icon: "icon-irr-subscription",
                    action: function() {
                        c._controlsGet("SHOW_NOTIFY")
                    }
                }, {
                    type: "separator"
                }, {
                    id: "irHelp",
                    type: "action",
                    label: h("HELP"),
                    hide: !0,
                    icon: "icon-irr-help",
                    action: function() {
                        e.popup.url(c.options.helpLink)
                    }
                }],
                beforeOpen: function(b, d) {
                    var e, g, i, j, k, l, m = d.menu.items, n = c.options;
                    if (c._dialogReset(),
                    c._sortWidgetHide(),
                    a(m, "irColumn").hide = !(n.selectColumns && "REPORT" === c.viewMode),
                    a(m, "irFilter").hide = !n.filter,
                    k = a(m, "irData"),
                    k.hide = !0,
                    l = k.menu.items,
                    "REPORT" === c.viewMode ? (n.sort || n.aggregate || n.flashback || n.compute) && (k.hide = !1,
                    a(l, "irOrdering").hide = !n.sort,
                    a(l, "irAggregate").hide = !n.aggregate,
                    a(l, "irFlashback").hide = !n.flashback,
                    a(l, "irCompute").hide = !n.compute,
                    a(l, "irGroupBySort").hide = !0,
                    a(l, "irPivotSort").hide = !0) : "GROUP_BY" === c.viewMode ? n.groupBy && (k.hide = !1,
                    a(l, "irOrdering").hide = !0,
                    a(l, "irAggregate").hide = !0,
                    a(l, "irFlashback").hide = !n.flashback,
                    a(l, "irCompute").hide = !0,
                    a(l, "irGroupBySort").hide = !1,
                    a(l, "irPivotSort").hide = !0) : "PIVOT" === c.viewMode ? n.pivot && (k.hide = !1,
                    a(l, "irOrdering").hide = !0,
                    a(l, "irAggregate").hide = !0,
                    a(l, "irFlashback").hide = !n.flashback,
                    a(l, "irCompute").hide = !0,
                    a(l, "irGroupBySort").hide = !0,
                    a(l, "irPivotSort").hide = !1) : "CHART" === c.viewMode && (k.hide = !1,
                    a(l, "irOrdering").hide = !0,
                    a(l, "irAggregate").hide = !0,
                    a(l, "irFlashback").hide = !n.flashback,
                    a(l, "irCompute").hide = !0,
                    a(l, "irGroupBySort").hide = !0,
                    a(l, "irPivotSort").hide = !0),
                    k = a(m, "irFormat"),
                    k.hide = !0,
                    l = k.menu.items,
                    "REPORT" === c.viewMode ? (n.controlBreak || n.highlight) && (k.hide = !1,
                    a(l, "irCtrlBreak").hide = !n.controlBreak,
                    a(l, "irHighlight").hide = !n.highlight,
                    a(l, "irRowsPerPage").hide = !n.rowsPerPage) : "GROUP_BY" === c.viewMode ? n.groupBy && (k.hide = !1,
                    a(l, "irCtrlBreak").hide = !0,
                    a(l, "irHighlight").hide = !0,
                    a(l, "irRowsPerPage").hide = !n.rowsPerPage) : "PIVOT" === c.viewMode ? n.pivot && (k.hide = !1,
                    a(l, "irCtrlBreak").hide = !0,
                    a(l, "irHighlight").hide = !0,
                    a(l, "irRowsPerPage").hide = !n.rowsPerPage) : "CHART" === c.viewMode && (k.hide = !1,
                    a(l, "irCtrlBreak").hide = !0,
                    a(l, "irHighlight").hide = !0,
                    a(l, "irRowsPerPage").hide = !n.rowsPerPage),
                    n.rowsPerPage) {
                        for (k = a(l, "irRowsPerPage"),
                        k.menu.items[0].choices = [],
                        i = k.menu.items[0].choices,
                        j = n.maxRowCount,
                        n.maxRowsPerPage && n.maxRowsPerPage < j && (j = n.maxRowsPerPage),
                        e = 0; e < f.length && (g = f[e],
                        !(g > j)); e++)
                            i.push({
                                label: "" + g,
                                value: g
                            });
                        n.maxRowsPerPage || i.push({
                            label: h("ALL"),
                            value: 1e5
                        })
                    }
                    "REPORT" === c.viewMode ? (n.chart || n.groupBy || n.pivot) && (a(m, "irChart").hide = !n.chart,
                    a(m, "irGroupBy").hide = !n.groupBy,
                    a(m, "irPivot").hide = !n.pivot) : "GROUP_BY" === c.viewMode ? n.groupBy && (a(m, "irChart").hide = !0,
                    a(m, "irGroupBy").hide = !1,
                    a(m, "irPivot").hide = !0) : "PIVOT" === c.viewMode ? n.pivot && (k.hide = !1,
                    a(m, "irChart").hide = !0,
                    a(m, "irGroupBy").hide = !0,
                    a(m, "irPivot").hide = !1) : "CHART" === c.viewMode && (k.hide = !1,
                    a(m, "irChart").hide = !1,
                    a(m, "irGroupBy").hide = !0,
                    a(m, "irPivot").hide = !0),
                    k = a(m, "irReport"),
                    k.hide = !0,
                    l = k.menu.items,
                    (n.saveReport || n.saveDefaultReport || n.reset) && (k.hide = !1,
                    a(l, "irSaveReport").hide = !n.saveReport,
                    a(l, "irSaveDefault").hide = !n.saveDefaultReport,
                    a(l, "irReset").hide = !n.reset),
                    "REPORT" !== c.viewMode && "GROUP_BY" !== c.viewMode && "PIVOT" !== c.viewMode || (a(m, "irDownload").hide = !n.download,
                    a(m, "irNotify").hide = !n.subscription),
                    a(m, "irHelp").hide = !n.help
                }
            } : {
                items: [{
                    id: "irColumn",
                    type: "action",
                    label: h("SELECT_COLUMNS"),
                    hide: !0,
                    icon: "icon-irr-select-cols",
                    action: function() {
                        c._controlsGet("SHOW_COLUMN", "COLUMN")
                    }
                }, {
                    type: "separator"
                }, {
                    id: "irFilter",
                    type: "action",
                    label: h("FILTER"),
                    hide: !0,
                    icon: "icon-irr-filter",
                    action: function() {
                        c._controlsGet("SHOW_FILTER")
                    }
                }, {
                    id: "irRowsPerPage",
                    type: "subMenu",
                    label: h("ROWS_PER_PAGE"),
                    hide: !0,
                    icon: "icon-irr-rows",
                    menu: {
                        items: [{
                            type: "radioGroup",
                            set: function(a) {
                                c.options.currentRowsPerPage = 1 * a,
                                c._search("SEARCH")
                            },
                            get: function() {
                                return c.options.currentRowsPerPage
                            },
                            choices: []
                        }]
                    }
                }, {
                    id: "irFormat",
                    type: "subMenu",
                    label: h("FORMAT"),
                    hide: !1,
                    icon: "icon-irr-format",
                    menu: {
                        items: [{
                            id: "irOrdering",
                            type: "action",
                            label: h("SORT"),
                            hide: !0,
                            icon: "icon-irr-sort",
                            action: function() {
                                c._controlsGet("SHOW_ORDERING")
                            }
                        }, {
                            id: "irCtrlBreak",
                            type: "action",
                            label: h("CONTROL_BREAK"),
                            hide: !0,
                            icon: "icon-irr-control-break",
                            action: function() {
                                c._controlsGet("SHOW_CTRL_BREAK")
                            }
                        }, {
                            id: "irHighlight",
                            type: "action",
                            label: h("HIGHLIGHT"),
                            hide: !0,
                            icon: "icon-irr-highlight",
                            action: function() {
                                c._controlsGet("SHOW_HIGHLIGHT")
                            }
                        }, {
                            id: "irCompute",
                            type: "action",
                            label: h("COMPUTE"),
                            hide: !0,
                            icon: "icon-irr-compute",
                            action: function() {
                                c._computationShow()
                            }
                        }, {
                            id: "irAggregate",
                            type: "action",
                            label: h("AGGREGATE"),
                            hide: !0,
                            icon: "icon-irr-aggregate",
                            action: function() {
                                c._controlsGet("SHOW_AGGREGATE")
                            }
                        }, {
                            id: "irChart",
                            type: "action",
                            label: h("CHART"),
                            hide: !0,
                            icon: "icon-irr-chart",
                            action: function() {
                                c._controlsGet("SHOW_CHART")
                            }
                        }, {
                            id: "irGroupBySort",
                            type: "action",
                            label: h("GROUP_BY_SORT"),
                            hide: !0,
                            icon: "icon-irr-sort",
                            action: function() {
                                c._controlsGet("SHOW_GROUP_BY_SORT")
                            }
                        }, {
                            id: "irGroupBy",
                            type: "action",
                            label: h("GROUP_BY"),
                            hide: !0,
                            icon: "icon-irr-group-by",
                            action: function() {
                                c._controlsGet("SHOW_GROUP_BY")
                            }
                        }, {
                            id: "irPivotSort",
                            type: "action",
                            label: h("PIVOT_SORT"),
                            hide: !0,
                            icon: "icon-irr-sort",
                            action: function() {
                                c._controlsGet("SHOW_PIVOT_SORT")
                            }
                        }, {
                            id: "irPivot",
                            type: "action",
                            label: h("PIVOT"),
                            hide: !0,
                            icon: "icon-irr-pivot",
                            action: function() {
                                c._controlsGet("SHOW_PIVOT")
                            }
                        }]
                    }
                }, {
                    type: "separator"
                }, {
                    id: "irFlashback",
                    type: "action",
                    label: h("FLASHBACK"),
                    hide: !0,
                    icon: "icon-irr-flashback",
                    action: function() {
                        c._controlsGet("SHOW_FLASHBACK")
                    }
                }, {
                    type: "separator"
                }, {
                    id: "irSaveReport",
                    type: "action",
                    label: h("SAVE_REPORT"),
                    hide: !0,
                    icon: "icon-irr-saved-report",
                    action: function() {
                        c._controlsGet("SAVE_REPORT")
                    }
                }, {
                    id: "irSaveDefault",
                    type: "action",
                    label: h("SAVE_REPORT_DEFAULT"),
                    hide: !0,
                    icon: "icon-irr-saved-report",
                    action: function() {
                        c._controlsGet("SHOW_SAVE_DEFAULT")
                    }
                }, {
                    id: "irReset",
                    type: "action",
                    label: h("RESET"),
                    hide: !0,
                    icon: "icon-irr-reset",
                    action: function() {
                        c._controlsGet("SHOW_RESET")
                    }
                }, {
                    type: "separator"
                }, {
                    id: "irHelp",
                    type: "action",
                    label: h("HELP"),
                    hide: !0,
                    icon: "icon-irr-help",
                    action: function() {
                        e.popup.url(c.options.helpLink)
                    }
                }, {
                    type: "separator"
                }, {
                    id: "irDownload",
                    type: "action",
                    label: h("DOWNLOAD"),
                    hide: !0,
                    icon: "icon-irr-download",
                    action: function() {
                        c._controlsGet("SHOW_DOWNLOAD")
                    }
                }, {
                    id: "irNotify",
                    type: "action",
                    label: h("SUBSCRIPTION"),
                    hide: !0,
                    icon: "icon-irr-subscription",
                    action: function() {
                        c._controlsGet("SHOW_NOTIFY")
                    }
                }],
                beforeOpen: function(b, d) {
                    var e, g, i, j, k, l, m = c.options, n = d.menu.items;
                    if (c._dialogReset(),
                    c._sortWidgetHide(),
                    a(n, "irColumn").hide = !(m.selectColumns && "REPORT" === c.viewMode),
                    a(n, "irFilter").hide = !m.filter,
                    a(n, "irRowsPerPage").hide = !m.rowsPerPage,
                    k = a(n, "irFormat"),
                    k.hide = !0,
                    l = k.menu.items,
                    "REPORT" === c.viewMode ? (m.sort || m.controlBreak || m.highlight || m.compute || m.aggregate || m.chart || m.groupBy || m.pivot) && (k.hide = !1,
                    a(l, "irOrdering").hide = !m.sort,
                    a(l, "irCtrlBreak").hide = !m.controlBreak,
                    a(l, "irHighlight").hide = !m.highlight,
                    a(l, "irCompute").hide = !m.compute,
                    a(l, "irAggregate").hide = !m.aggregate,
                    a(l, "irChart").hide = !m.chart,
                    a(l, "irGroupBySort").hide = !0,
                    a(l, "irGroupBy").hide = !m.groupBy,
                    a(l, "irPivotSort").hide = !0,
                    a(l, "irPivot").hide = !m.pivot) : "GROUP_BY" === c.viewMode ? m.groupBy && (k.hide = !1,
                    a(l, "irOrdering").hide = !0,
                    a(l, "irCtrlBreak").hide = !0,
                    a(l, "irHighlight").hide = !0,
                    a(l, "irCompute").hide = !0,
                    a(l, "irAggregate").hide = !0,
                    a(l, "irChart").hide = !0,
                    a(l, "irGroupBySort").hide = !1,
                    a(l, "irGroupBy").hide = !1,
                    a(l, "irPivotSort").hide = !0,
                    a(l, "irPivot").hide = !0) : "PIVOT" === c.viewMode ? m.pivot && (k.hide = !1,
                    a(l, "irOrdering").hide = !0,
                    a(l, "irCtrlBreak").hide = !0,
                    a(l, "irHighlight").hide = !0,
                    a(l, "irCompute").hide = !0,
                    a(l, "irAggregate").hide = !0,
                    a(l, "irChart").hide = !0,
                    a(l, "irGroupBySort").hide = !0,
                    a(l, "irGroupBy").hide = !0,
                    a(l, "irPivotSort").hide = !1,
                    a(l, "irPivot").hide = !1) : "CHART" === c.viewMode && (k.hide = !1,
                    a(l, "irOrdering").hide = !0,
                    a(l, "irCtrlBreak").hide = !0,
                    a(l, "irHighlight").hide = !0,
                    a(l, "irCompute").hide = !0,
                    a(l, "irAggregate").hide = !0,
                    a(l, "irChart").hide = !1,
                    a(l, "irGroupBySort").hide = !0,
                    a(l, "irGroupBy").hide = !0,
                    a(l, "irPivotSort").hide = !0,
                    a(l, "irPivot").hide = !0),
                    a(n, "irFlashback").hide = !m.flashback,
                    a(n, "irSaveReport").hide = !m.saveReport,
                    a(n, "irSaveDefault").hide = !m.saveDefaultReport,
                    a(n, "irReset").hide = !m.reset,
                    a(n, "irHelp").hide = !m.help,
                    "REPORT" !== c.viewMode && "GROUP_BY" !== c.viewMode && "PIVOT" !== c.viewMode || (a(n, "irDownload").hide = !m.download,
                    a(n, "irNotify").hide = !m.subscription),
                    m.rowsPerPage) {
                        for (k = a(n, "irRowsPerPage"),
                        k.menu.items[0].choices = [],
                        i = k.menu.items[0].choices,
                        j = m.maxRowCount,
                        m.maxRowsPerPage && m.maxRowsPerPage < j && (j = m.maxRowsPerPage),
                        e = 0; e < f.length && (g = f[e],
                        !(g > j)); e++)
                            i.push({
                                label: "" + g,
                                value: g
                            });
                        m.maxRowsPerPage || i.push({
                            label: h("ALL"),
                            value: 1e5
                        })
                    }
                }
            },
            d.toolbar && d.actionsMenu && c._getElement("actions_menu").menu(b)
        },
        _initOnCreate: function() {
            var b = this.options
              , c = this;
            b.toolbar && this._initToolbar(!0),
            this._initControlPanel(),
            a(document.body).append(this._getElement("sort_widget")),
            this._on(this.element, {
                "click a.a-IRR-headerLink": function(b) {
                    "REPORT" === this.viewMode ? this._controlsGet("SORT_WIDGET", a(b.currentTarget).data("column")) : "GROUP_BY" === this.viewMode ? this._controlsGet("SHOW_GROUP_BY_SORT") : "PIVOT" === this.viewMode && this._controlsGet("SHOW_PIVOT_SORT"),
                    b.preventDefault()
                }
            }),
            this._on(this.element, {
                "click button.a-IRR-button--pagination": function(c) {
                    b.detailLink && "SHOW_DETAIL" === this.currentControl ? this._controlsRow(a(c.currentTarget).data("row-id")) : b.pagination && this._paginate(a(c.currentTarget).data("pagination"))
                },
                "click a.a-IRR-pagination-reset": function(a) {
                    this._search("SEARCH"),
                    a.preventDefault()
                }
            }),
            b.pagination && this._on(this.element, {
                "click a.a-IRR-pagination-reset": function(a) {
                    this._search("SEARCH"),
                    a.preventDefault()
                }
            }),
            b.detailLink && this._on(this.element, {
                "click a.a-IRR-detail-row": function(b) {
                    this._controlsRow(a(b.currentTarget).data("row-id")),
                    b.preventDefault()
                }
            }),
            this._initFixedHeader(),
            apex.widget.util.onVisibilityChange(this.element[0], function(a) {
                a && c.element.find(".js-stickyTableHeader").trigger("forceresize")
            })
        },
        _initToolbar: function(b) {
            var c = this.options
              , d = this;
            c.searchField && (this._on(this._getElement("search_field"), {
                keydown: function(b) {
                    b.which === a.ui.keyCode.ENTER && (this._search("SEARCH"),
                    b.preventDefault())
                }
            }),
            this._on(this._getElement("search_button"), {
                click: function(a) {
                    this._search("SEARCH"),
                    a.preventDefault()
                }
            }),
            c.columnSearch && b && this._getElement("column_search_drop").menu({
                asyncFetchMenu: function(a, b) {
                    d.searchMenu = a,
                    d.searchMenuCallback = b,
                    d._controlsGet("SEARCH_COLUMN")
                },
                afterClose: function(a, b) {
                    b.actionTaken && setTimeout(function() {
                        d._getElement("search_field").focus()
                    }, 100)
                },
                items: []
            })),
            c.rowsPerPageSelect && this._on(this._getElement("row_select"), {
                change: function(a) {
                    var b = a.target.value;
                    this._search("SEARCH", b),
                    a.preventDefault()
                }
            }),
            c.reportsSelect && this._on(this._getElement("saved_reports"), {
                change: function(a) {
                    var b = a.target.value;
                    this._pull("REPORT_CHANGED", b),
                    a.preventDefault()
                }
            }),
            this._on(this._getElement("toolbar_controls"), {
                "click .a-IRR-button--views": function(b) {
                    var c = a(b.currentTarget).data("view");
                    switch (c) {
                    case "report":
                        this._reportView("REPORT");
                        break;
                    case "icon":
                        this._reportView("ICON");
                        break;
                    case "details":
                        this._reportView("DETAIL");
                        break;
                    case "chart":
                        this._chartView();
                        break;
                    case "group_by":
                        this._groupByView();
                        break;
                    case "pivot":
                        this._pivotView()
                    }
                }
            }),
            c.actionsMenu && b && this._initMenus()
        },
        _inlinePicker: function(c, d) {
            var e, f, g = b.htmlBuilder(), h = a.parseJSON(d), i = a("[data-picker-for=" + b.escapeCSS(this.tempReturnElement$.attr("id")) + "]", this._getElement("dialog_js"));
            for (g.markup("<div").attr("id", this._getId("col_values_drop")).attr("class", "a-IRR-col-values-drop").markup(">"),
            e = 0; e < h.row.length; e++)
                g.markup("<a").attr("href", "#").attr("class", z).attr("data-return-value", h.row[e].R).markup(">").markup(h.row[e].D).markup("</a>");
            return g.markup("</div>"),
            i.after(g.toString()),
            f = this._getDialogElement("col_values_drop"),
            "NARROW" === c ? this._on(f, {
                "click a.a-IRR-col-value": function(b) {
                    var c, d = a(b.currentTarget).data("returnValue"), e = this._dialogCurrentOperator().val();
                    "in" === e || "not in" === e ? (c = this.tempReturnElement$.val(),
                    c && (d = c + "," + d),
                    this.tempReturnElement$.val(d)) : (this.tempReturnElement$.val(d),
                    f.remove(),
                    this.tempReturnElement$.focus()),
                    b.preventDefault()
                }
            }) : this._on(f, {
                "click a.a-IRR-col-value": function(b) {
                    var c = a(b.currentTarget).data("returnValue");
                    this.tempReturnElement$.val(c),
                    f.remove(),
                    this.tempReturnElement$.focus(),
                    b.preventDefault()
                }
            }),
            this.suppressUpdate = !1,
            this.currentAction = null,
            this._on(f, {
                "keydown a": function(b) {
                    var c = f.find("a")
                      , d = c.index(a(b.target))
                      , e = c.length - 1;
                    switch (c.attr("tabindex", -1),
                    b.which) {
                    case a.ui.keyCode.DOWN:
                        d < e ? c.eq(d + 1).focus() : c.eq(0).focus(),
                        b.preventDefault();
                        break;
                    case a.ui.keyCode.UP:
                        d > 0 ? c.eq(d - 1).focus() : c.eq(e).focus(),
                        b.preventDefault();
                        break;
                    case a.ui.keyCode.TAB:
                        f.remove(),
                        i.focus(),
                        b.preventDefault();
                        break;
                    case a.ui.keyCode.ESCAPE:
                        f.remove(),
                        i.focus(),
                        b.stopImmediatePropagation()
                    }
                }
            }),
            this._dialogCheck(this._getIdSelector("col_values_drop"), function() {
                f.remove()
            }),
            f.find("a:first")
        },
        _paginate: function(a) {
            this._action("PAGE", {
                widgetActionMod: a
            })
        },
        _notifyClear: function() {
            this._action("DELETE_NOTIFY", {
                id: this._getDialogElement("notify_id").val()
            })
        },
        _notifySave: function() {
            var a = [this._getId("notify_id"), this._getId("email_address"), this._getId("email_subject"), this._getId("notify_interval"), this._getId("start_date"), this._getId("end_date")];
            this.suppressUpdate = !0,
            this._action("SAVE_NOTIFY", {
                f01: a,
                f02: this._utilGetFormElValues(a)
            })
        },
        _pivotMaxValue: 3,
        _pivotRemove: function() {
            this._action("DELETE_PIVOT")
        },
        _pivotSave: function() {
            var a = this._utilGetFormElAttributes();
            this.suppressUpdate = !0,
            this._action("SAVE_PIVOT", {
                f01: a.ids,
                f02: a.values
            })
        },
        _pivotSort: function(a) {
            var b, c = this._getDialogElement("pivot_id").val();
            "ASC" === a || "DESC" === a ? (this.lastColumnId = a.id,
            this._action("PIVOT_COLUMN_SORT", {
                id: c,
                f01: this.lastColumnId,
                f02: a
            })) : (b = this._utilGetFormElAttributes(),
            this._action("PIVOT_SORT", {
                id: c,
                f01: b.ids,
                f02: b.values
            }))
        },
        _pivotView: function() {
            this._action("VIEW_PIVOT")
        },
        _pull: function(b, c, d) {
            var e = a.extend({
                widgetMod: "PULL",
                widgetAction: b
            }, d);
            c && (this.reportId = c),
            this.currentAction = b,
            this._get(e)
        },
        _remove: function(a) {
            var b = "DELETE";
            a && (b = a),
            this._action(b)
        },
        _reportView: function(a) {
            this.options.reportViewMode = a,
            this._action("VIEW_REPORT", {
                p_widget_view_mode: this.options.reportViewMode
            })
        },
        _reset: function() {
            this._action("RESET")
        },
        _save: function(a) {
            var b, c = [], d = "SAVE", e = this._getId("report_name"), f = $f_get_emptys([e], "error", "");
            this.options.saveReportCategory && (b = $x(this._getId("new_category")),
            b && (f = $f_get_emptys([b], "error", ""))),
            f || (a && (d = "RENAME"),
            this.options.saveReportCategory && (c.push(this._getId("report_category")),
            c.push(this._getId("new_category"))),
            c.push(e),
            c.push(this._getId("public_report")),
            c.push(this._getId("report_description")),
            this._action(d, {
                f01: c,
                f02: this._utilGetFormElValues(c)
            }),
            this._getElement("dialog_js").dialog("close"))
        },
        _saveCategoryCheck: function(b) {
            var c = this._getId("new_category");
            "new" === b.value ? a("<input/>", {
                id: c,
                type: "text",
                title: h("NEW_CATEGORY_LABEL"),
                name: ""
            }).insertAfter(b) : this._getDialogElement("new_category").remove()
        },
        _saveDefault: function(a) {
            var b, c = [], d = [], e = "SAVE_DEFAULT", f = this._getId("default_type"), g = $v(f), h = this._getId("report_name");
            "ALTERNATIVE" === g && (b = $f_get_emptys([h], "error", "")),
            b || (a && (e = a),
            c.push(f),
            d.push(g),
            "ALTERNATIVE" === g && (c.push(h),
            d.push(this._getDialogElement("report_name").val())),
            this._action(e, {
                f01: c,
                f02: d
            }),
            this._getElement("dialog_js").dialog("close"))
        },
        _saveDefaultTypeCheck: function(a) {
            var b = "ALTERNATIVE" === a;
            this._getDialogElement("report_name").closest("tr").toggle(b)
        },
        _search: function(a, b) {
            var c, d, e = this.options, f = this._getElement("search_field").val();
            b && (e.rowsPerPage || e.rowsPerPageSelect) && (e.currentRowsPerPage = 1 * b),
            d = this._utilGetFormElAttributes(this._getId("toolbar_controls")),
            c = {
                f01: d.ids,
                f02: d.values
            },
            "" === f ? this._pull(null, this.reportId, c) : this._action("QUICK_FILTER", c)
        },
        _setDateFieldFormatMask: function(a, b) {
            var c, d, e, f = !1;
            a.length > 0 && b && (/HH|hh|ii|ss/.test(b) && (f = !0,
            c = /HH/.test(b)),
            d = a.val(),
            e = a.datepicker("option", "dateFormat"),
            a.datepicker("option", "onSelect", null),
            a.datepicker("option", "showTime", f).datepicker("option", "showButtonPanel", f).datepicker("option", "dateFormat", b),
            f && a.datepicker("option", "time24h", c),
            a.val(""),
            b === e && a.val(d))
        },
        _singleRowViewClear: function() {
            var a = this._getElement("single_row_view")
              , b = this._getElement("report_view");
            return this._off(a),
            this._off(b),
            a.html(""),
            a
        },
        _singleRowViewControl: function() {
            var b = this._getElement("exclude_nulls")
              , c = this._getElement("show_displayed_only")
              , d = b.prop("checked")
              , e = c.prop("checked")
              , f = a("div.a-IRR-singleRow-row", this.element)
              , g = f.filter(".is-displayed")
              , h = f.not(".is-displayed, .is-null")
              , i = f.filter(".is-null");
            this.ajaxBusy || (g.show(),
            h.show(),
            d && e ? (i.hide(),
            h.hide()) : d ? i.hide() : e && h.hide(),
            this.currentAction = "CHANGE_DETAIL_OPTION",
            this.suppressUpdate = !0,
            this._action("CHANGE_DETAIL_OPTION", {
                value: d ? b.val() : "",
                x05: e ? c.val() : ""
            }))
        },
        _singleRowViewHide: function() {
            this._singleRowViewClear().hide()
        },
        _singleRowViewShow: function(b) {
            var c = this._singleRowViewClear();
            this._getElement("full_view").hide(),
            this._getElement("data_panel").val(""),
            this._getElement("dialog_js").html(""),
            c.html(b).show(),
            c.find(":focusable")[0].focus(),
            this.options.detailLink && (this._on(this._getElement("report_view"), {
                click: function(b) {
                    this._pull(null, a(b.target).data("report-id"))
                }
            }),
            this._on(c, {
                "click input.a-IRR-viewOptions-checkbox": function() {
                    this._singleRowViewControl()
                }
            }),
            a("." + A).collapsible({
                collapsed: !1
            }))
        },
        _sortWidgetHide: function() {
            var b, c, d, e = this._getElement("sort_widget");
            e.is(":visible") && (b = this._getElement("sort_widget_rows"),
            c = this._getElement("sort_widget_search_field"),
            d = a("[data-column=" + this.lastColumnId + "]", this.element),
            e.removeAttr("style").css({
                position: "absolute",
                display: "none"
            }),
            d.closest(".a-IRR-header").removeClass("is-active"),
            b.html(""),
            a("button.a-IRR-sortWidget-button", this.element).removeClass("is-active"),
            this._off(e),
            this._off(b),
            this._off(c))
        },
        _sortWidgetSearch: function(a, b) {
            var c = b ? "contains" : "="
              , d = [this.currentColumnId, c, a, "", ""];
            this._sortWidgetHide(),
            this._action("COL_FILTER", {
                f01: d
            })
        },
        _sortWidgetShow: function(c) {
            function d(a) {
                var b = m.find(":focusable");
                a || (f = b.first(),
                f.data("first", !0)),
                g = b.last(),
                g.data("last", !0)
            }
            var e, f, g, h, i, k = a.parseJSON(c), l = b.htmlBuilder(), m = this._getElement("sort_widget"), o = this._getElement("sort_widget_help"), p = this._getElement("sort_widget_rows"), q = a("[data-column='" + this.currentColumnId + "']", this.element), r = this._getElement("sort_widget_search"), s = this._getElement("sort_widget_search_field");
            if (this.computationId = k.dialog.id,
            o.hide(),
            a("button." + n, m).parent().show(),
            a.each(k.dialog.hide, function(b, c) {
                a(j(c), m).hide()
            }),
            k.dialog.leadSortDir && ("ASC" === k.dialog.leadSortDir ? this._getElement("sort_widget_action_up").find("button.a-IRR-sortWidget-button").addClass("is-active") : "DESC" === k.dialog.leadSortDir && this._getElement("sort_widget_action_down").find("button.a-IRR-sortWidget-button").addClass("is-active")),
            k.dialog.uv) {
                for (h = k.dialog.row.length,
                e = 0; e < h; e++)
                    (0 === k.dialog.row[e].R || k.dialog.row[e].R) && (i = 0 === k.dialog.row[e].D || k.dialog.row[e].D ? k.dialog.row[e].D : k.dialog.row[e].R,
                    l.markup("<a").attr("href", "#").attr("data-return-value", k.dialog.row[e].R).attr("class", "a-IRR-sortWidget-row").markup(">").markup(i).markup("</a>"));
                p.append(l.toString()),
                r.show(),
                s.val("")
            } else
                r.hide();
            m.show().position({
                my: "left top",
                at: "left bottom",
                of: q
            }),
            q.closest(".a-IRR-header").addClass("is-active"),
            this.lastColumnId = this.currentColumnId,
            this._on(m, {
                "click button.a-IRR-sortWidget-button": function(b) {
                    var c = a(b.currentTarget).data("option");
                    switch (c) {
                    case "up":
                        this._columnOrder("ASC");
                        break;
                    case "down":
                        this._columnOrder("DESC");
                        break;
                    case "hide":
                        this._columnHide();
                        break;
                    case "break":
                        this._controlBreakOn();
                        break;
                    case "help":
                        this._columnHelp();
                        break;
                    case "computation":
                        this._computationShow()
                    }
                },
                keydown: function(b) {
                    if (b.which === a.ui.keyCode.ESCAPE && (this._sortWidgetHide(),
                    b.preventDefault(),
                    q.focus()),
                    b.which === a.ui.keyCode.TAB) {
                        var c = !!b.shiftKey;
                        !c && a(b.target).data("last") && (b.preventDefault(),
                        f.focus()),
                        c && a(b.target).data("first") && (b.preventDefault(),
                        g.focus())
                    }
                }
            }),
            this._on(p, {
                "click a": function(b) {
                    this._sortWidgetSearch(a(b.currentTarget).data("returnValue")),
                    b.preventDefault()
                }
            }),
            this._on(s, {
                keyup: function(a) {
                    g.data("last", !1),
                    $d_Find(this._getId("sort_widget_rows"), a.target.value, "a"),
                    d(!0)
                },
                keydown: function(b) {
                    b.which === a.ui.keyCode.ENTER && (this._sortWidgetSearch(a(b.target).val(), !0),
                    b.preventDefault())
                }
            }),
            this._dialogCheck(null, this._sortWidgetHide),
            d(),
            f.focus()
        },
        _utilGetFormEls: function(b) {
            return a(j(b) + " :input").not("button")
        },
        _utilGetFormElAttributes: function(a) {
            var b, c = [], d = [];
            return b = a ? a : this._getId("dialog_js"),
            this._utilGetFormEls(b).each(function(a, b) {
                c.push(b.id),
                d.push($v(b.id))
            }),
            {
                ids: c,
                values: d
            }
        },
        _utilGetFormElValues: function(a) {
            var b, c = [];
            for (b = 0; b < a.length; b++)
                c.push($v(a[b]));
            return c
        },
        _utilReplaceAttrText: function(a, b, c, d) {
            var e = a.attr(b).replace(c, d);
            a.attr(b, e)
        },
        _utilAddMoreColumn: function(b, c) {
            var d, e, f, g, h, i, j, k, l = this._getElement("dialog_js");
            d = a("select." + c, l).length,
            d < b && (e = d,
            f = ++d,
            e < 10 ? (g = "0" + e,
            h = "0" + f) : (g = e + "",
            h = f + ""),
            i = a("tr." + c + "-row-" + e, l),
            j = i.clone(),
            this._utilReplaceAttrText(j, "class", e, f),
            a("." + r, j).text(f),
            k = a("select." + c, j),
            this._utilReplaceAttrText(k, "id", new RegExp(g + "$"), h),
            this._utilReplaceAttrText(k, "title", e, f),
            j.insertAfter(i)),
            f === b && (a("tr." + c + "-add", l).hide(),
            j.focus())
        },
        _utilAddMoreFunction: function(b) {
            var c, d, e, f, g, h, i, j, k, l, m, n, o, p, r = this._getElement("dialog_js");
            c = a("select." + s, r).length,
            c < b && (d = c,
            e = ++c,
            d < 10 ? (f = "0" + d,
            g = "0" + e) : (f = d + "",
            g = e + ""),
            h = a("tr." + w + d, r),
            i = h.clone(),
            this._utilReplaceAttrText(i, "class", d, e),
            a("span." + u, i).text(e),
            j = a("select." + s, i),
            this._utilReplaceAttrText(j, "title", d, e),
            this._utilReplaceAttrText(j, "id", new RegExp(f + "$"), g),
            this._utilReplaceAttrText(a(this._getIdSelector("number_columns_container") + "_" + f, i), "id", new RegExp(f + "$"), g),
            this._utilReplaceAttrText(a(this._getIdSelector("all_columns_container") + "_" + f, i), "id", new RegExp(f + "$"), g),
            k = a("select." + v, i),
            this._utilReplaceAttrText(k, "title", d, e),
            this._utilReplaceAttrText(k, "id", new RegExp(f + "$"), g),
            l = a("select." + t, i),
            this._utilReplaceAttrText(l, "title", d, e),
            this._utilReplaceAttrText(l, "id", new RegExp(f + "$"), g),
            m = a(this._getIdSelector("label") + "_" + f, i),
            this._utilReplaceAttrText(m, "title", d, e),
            this._utilReplaceAttrText(m, "id", new RegExp(f + "$"), g),
            m.val(""),
            n = a(this._getIdSelector("format_mask") + "_" + f, i),
            this._utilReplaceAttrText(n, "title", d, e),
            this._utilReplaceAttrText(n, "id", new RegExp(f + "$"), g),
            n.val(""),
            o = a(this._getIdSelector("format_mask_picker") + "_" + f, i),
            this._utilReplaceAttrText(o, "id", new RegExp(f + "$"), g),
            this._utilReplaceAttrText(o, "data-picker-for", new RegExp(f + "$"), g),
            p = a(this._getIdSelector("function_sum") + "_" + f, i),
            this._utilReplaceAttrText(p, "title", d, e),
            this._utilReplaceAttrText(p, "id", new RegExp(f + "$"), g),
            p.prop("checked", !1),
            i.insertAfter(h)),
            e === b && (a("tr." + q, r).hide(),
            i.focus())
        },
        _validAction: function(a) {
            "true" === a ? (this._pull("PULL_TOOLBAR"),
            this._getElement("dialog_js").dialog("close")) : (this._getDialogElement("dialog_msg").html(a),
            this.options.reportViewMode = "REPORT")
        },
        refresh: function() {
            this._pull()
        }
    })
}(apex.jQuery, apex.util, apex.debug, apex.server, apex.navigation, apex.lang);

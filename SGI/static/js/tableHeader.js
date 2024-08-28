!function(a, b) {
    "use strict";
    function c(c, d) {
        var e, f, g = c.find("div.t-fht-thead"), h = c.find("div.t-fht-tbody"), i = g.find("table th:last-child").first();
        0 === g.find("th.t-fht-thead-scroll").length && (e = a(document.createElement("th")),
        e.addClass("t-fht-thead-scroll"),
        f = b.getScrollbarSize().width,
        i.after(e),
        e.css({
            width: f,
            "min-width": f,
            "max-width": f,
            margin: "0px",
            padding: "0px"
        }),
        h.height(d))
    }
    function d(a, b, c) {
        function d(a, b) {
            var c;
            return a.length >= 1 && (c = window.getComputedStyle(a.get(0)).getPropertyValue(b)),
            c
        }
        var f, g, h;
        return g = parseInt(d(c, "height")),
        g || (g = c.height()),
        f = "collapse" === d(b, "border-collapse") ? 1 : 0,
        h = g + f,
        a !== e && b.height() - h > a
    }
    var e = -1
      , f = !1;
    a.fn.setTableHeadersAsFixed = function(b) {
        var g, h, i = /MSIE \d/.test(navigator.userAgent), j = /Trident\/(?:[7-9]|\d{2,})\..*rv:(\d+)/.exec(navigator.userAgent), k = i || j;
        if (f || (a("head").append('<style type="text/css">.t-fht-cell { height: 1px; overflow: hidden; } .t-fht-wrapper { width: 100%; overflow: hidden; position: relative; } .t-fht-thead { overflow: hidden; position: relative; } .t-fht-tbody { overflow: auto; } </style>'),
        f = !0),
        window.getComputedStyle || (window.getComputedStyle = function(a, b) {
            return this.el = a,
            this.getPropertyValue = function(b) {
                var c = /(\-([a-z]){1})/g;
                return "float" == b && (b = "styleFloat"),
                c.test(b) && (b = b.replace(c, function() {
                    return arguments[2].toUpperCase()
                })),
                a.currentStyle[b] ? a.currentStyle[b] : null
            }
            ,
            this
        }
        ),
        g = this,
        g.is("table") || (g = this.find("table")),
        g.length > 0)
            return b = a.extend({}, {
                maxHeight: e
            }, b),
            h = 0,
            g.each(function(f, g) {
                var i, j, l, m, n, o, p, q, r = b.maxHeight, s = a(g);
                h += 1,
                r == e && (s.hasClass("mxh480") ? r = 480 : s.hasClass("mxh320") ? r = 320 : s.hasClass("mxh480") && (r = 640)),
                i = s.find("tr").first(),
                i.find("th").each(function() {
                    var b = a(this);
                    b.append(a(document.createElement("div")).addClass("t-fht-cell"))
                }),
                j = a(document.createElement("div")).addClass("t-fht-wrapper"),
                l = a(document.createElement("div")).addClass("t-fht-thead"),
                l.attr("id", "stickyTableHeader_" + h),
                l.addClass("js-stickyTableHeader"),
                m = s.wrap(a(document.createElement("div")).addClass("t-fht-tbody")).parent(),
                n = s.clone().empty().append(i.clone(!0)).attr("role", "presentation"),
                l.append(n),
                m.before(l),
                j = l.add(m).wrapAll(j).parent(),
                d(r, s, i) && c(j, r),
                m.scroll(function() {
                    l.scrollLeft(this.scrollLeft)
                }),
                l.scroll(function() {
                    m.scrollLeft(this.scrollLeft)
                }),
                o = l.find("tr").first().find("th"),
                p = s.find("tr").first(),
                q = p.find("td"),
                q.length < 1 && (q = p.find("th")),
                q.each(function() {
                    a(this).removeAttr("id").css("visibility", "hidden")
                });
                var t = function() {
                    a(".js-stickyTableHeader").next().width("auto"),
                    q.each(function(b) {
                        var c = a(this).width();
                        k && (b + 1) % 6 === 0 && (c -= 1);
                        var d = o.eq(b);
                        d.find(".t-fht-cell").width(c),
                        b++
                    }),
                    s.css("margin-top", -s.find("tr").first().height()),
                    d(r, s, i) && c(j, r)
                };
                a(window).on("apexwindowresized", t),
                l.on("forceresize", t),
                t()
            }),
            this
    }
}(apex.jQuery, apex.util);

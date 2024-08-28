!function(a, b) {
    "use strict";
    var c, d = 300;
    a.widget("apex.stickyWidget", {
        version: "5.1",
        widgetEventPrefix: "stickyWidget",
        options: {
            zIndexStart: -1,
            toggleHeight: !1,
            toggleWidth: !1,
            top: null,
            bottom: null,
            stickToEnd: !1,
            useWindow: !0,
            isFooter: !1,
            stick: null,
            unstick: null,
            stickEnd: null,
            unstickEnd: null
        },
        reStick: function(a) {
            (this.stuck && !this.stuckToEnd || a) && (this.options.isFooter ? this.element.css("position", "fixed").css("bottom", 0) : this.element.css("position", "fixed").css("top", this.options.top(this)))
        },
        forceScrollParent: function(a) {
            this._destroy(),
            c = a && a.length > 0 ? a : null,
            this.stuck = !1,
            this._create()
        },
        _stickToEnd: function() {
            var a, b, c;
            this.stuckToEnd || (this.stuckToEnd = !0,
            b = this.element,
            this.options.isFooter ? (a = this.options.top.call(this),
            c = "bottom") : (a = this.options.bottom.call(this) - b.outerHeight(),
            c = "top"),
            b.css("bottom", ""),
            b.css("position", "absolute"),
            b.css("top", a - b.offsetParent().offset().top),
            this._trigger("stickEnd", null, {
                where: c,
                offset: a
            }))
        },
        _unstickFromEnd: function() {
            this.stuckToEnd && (this.stuckToEnd = !1,
            this.options.isFooter && this.element.css("top", ""),
            this.stuck ? (this.stuck = !1,
            this._stick()) : (this.stuck = !0,
            this._unstick()),
            this._trigger("unstickEnd", null, {
                where: this.options.isFooter ? "bottom" : "top"
            }))
        },
        _stick: function() {
            if (!this.stuck) {
                var a = this.element;
                a.addClass("is-stuck"),
                this.reStick(!0),
                this.stuck = !0,
                this.options.toggleHeight && a.css("height", this.unstuckHeight),
                this.options.toggleWidth && a.css("width", this.unstuckWidth),
                this.options.isFooter ? this._trigger("stick", null, {
                    where: "bottom",
                    offset: this.element.css("bottom")
                }) : this._trigger("stick", null, {
                    where: "top",
                    offset: this.element.css("top")
                })
            }
        },
        _unstick: function() {
            if (this.stuck) {
                var a = this.element;
                a.removeClass("is-stuck"),
                a.css("position", "absolute"),
                a.css(this.options.isFooter ? "bottom" : "top", "auto"),
                this.stuck = !1,
                this._revertToCssWidthAndHeight(),
                this._recalculateFixedStuckDimensions(),
                this._trigger("unstick", null, {
                    where: this.options.isFooter ? "bottom" : "top"
                })
            }
        },
        _revertToCssWidthAndHeight: function() {
            this.options.toggleHeight && this.element.css("height", this.cssHeight),
            this.options.toggleWidth && this.element.css("width", this.cssWidth)
        },
        _recalculateFixedStuckDimensions: function() {
            this.stuck || (this.unstuckWidth = this.element.outerWidth(),
            this.unstuckHeight = this.element.outerHeight())
        },
        _setupDimensions: function() {
            this._revertToCssWidthAndHeight(),
            this.replacement.css("width", this.element.outerWidth()).css("height", this.element.outerHeight())
        },
        refresh: function() {},
        handler: null,
        replacement: null,
        _deferCreate: function() {
            var b = this.options
              , e = this.replacement = a("<div></div>")
              , f = this.element;
            c ? this.scrollParent$ = c : (this.scrollParent$ = f.scrollParent(),
            b.useWindow && (this.scrollParent$ = a(window)));
            var g = this.isWindow = this.scrollParent$[0] === window
              , h = this.scrollParent$;
            f.addClass("js-stickyWidget-toggle"),
            b.zIndexStart === -1 ? this.zIndex = d++ : this.zIndex = b.zIndexStart,
            f.css("z-index", this.zIndex),
            e.insertAfter(f);
            var i = this;
            this._recalculateFixedStuckDimensions(),
            this.cssHeight = f.css("height"),
            this.cssWidth = f.css("width"),
            this._setupDimensions(),
            b.isFooter ? this.scrollHandler = function() {
                var a, c, d, j = h.scrollTop() + h.height() - b.bottom.call(i);
                if (b.stickToEnd) {
                    if (c = j - f.outerHeight(),
                    d = b.top.call(i),
                    c < d)
                        return void i._stickToEnd();
                    i._unstickFromEnd()
                }
                a = e.offset().top + e.outerHeight(),
                g || (a += h.scrollTop()),
                j < a ? i._stick() : i._unstick()
            }
            : this.scrollHandler = function() {
                var a, c, d, j = h.scrollTop() + b.top.call(i);
                if (b.stickToEnd) {
                    if (c = j + f.outerHeight(),
                    d = b.bottom.call(i),
                    c >= d)
                        return void i._stickToEnd();
                    i._unstickFromEnd()
                }
                a = e.offset().top,
                g || (a += h.scrollTop()),
                j >= a ? i._stick() : i._unstick()
            }
            ,
            this.refresh = this.resizeHandler = function() {
                i._destroy(),
                i.stuck = !1,
                i._create()
            }
            ,
            h.on("scroll", this.scrollHandler),
            a(window).on("apexwindowresized", this.resizeHandler),
            f.on("forceresize", this.resizeHandler),
            f.css("position", "absolute"),
            f.css(b.isFooter ? "bottom" : "top", "auto"),
            this.scrollHandler()
        },
        _createDebouncer: null,
        _create: function() {
            var b = this
              , c = this.options;
            this.stuck = !1,
            this.stuckToEnd = !1,
            this.cssWidth = 0,
            this.cssHeight = 0,
            this.unstuckWidth = 0,
            this.unstuckHeight = 0,
            c.isFooter ? (c.top || (c.top = function() {
                var b = a(this.element).parent()
                  , c = b.offset().top;
                return this.isWindow || (c -= this.scrollParent$.offset().top - this.scrollParent$.scrollTop()),
                c
            }
            ),
            c.bottom || (c.bottom = function() {
                return 0
            }
            )) : (c.top || (c.top = function() {
                return apex.theme.defaultStickyTop()
            }
            ),
            c.bottom || (c.bottom = function() {
                var b = a(this.element).parent()
                  , c = b.offset().top;
                return this.isWindow || (c -= this.scrollParent$.offset().top - this.scrollParent$.scrollTop()),
                c + b.outerHeight()
            }
            )),
            this._createDebouncer && clearTimeout(this._createDebouncer),
            this._createDebouncer = setTimeout(function() {
                b._deferCreate()
            }, 500)
        },
        _destroy: function() {
            this.scrollParent$.off("scroll", this.scrollHandler),
            a(window).off("apexwindowresized", this.resizeHandler),
            this.element.off("forceresize", this.resizeHandler),
            this.replacement.remove(),
            this.element.removeAttr("style")
        }
    })
}(apex.jQuery);

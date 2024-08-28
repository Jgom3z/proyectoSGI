!function(a, b, c, d) {
    "use strict";
    function e(a, b) {
        var d, e, f = "", g = a.className.split(" ");
        for (d = 0; d < g.length; d++)
            e = g[d],
            c.inArray(e, b) >= 0 && (f += " " + e);
        a.className = f.substr(1)
    }
    function f(a) {
        return a.parent().children(":visible").index(a)
    }
    function g(a) {
        var b = a.get(0).id;
        return b.substring(b.lastIndexOf("_") + 1)
    }
    function h(a, b) {
        return parseInt(a.children(y).find(b).attr(V), 10)
    }
    function i(a, b) {
        return parseInt(a.find(b).attr(V), 10)
    }
    function j(a, b, c, d, e) {
        var f, g, h;
        c.renderNodeContent ? c.renderNodeContent(b, a, d, e) : (c.getIcon && (f = c.getIcon(b),
        null !== f && a.markup("<span").attr("class", d.iconType + " " + f).markup("></span>")),
        g = d.useLinks && c.getLink && c.getLink(b),
        h = g ? "a" : "span",
        a.markup("<" + h + " tabIndex='-1' role='treeitem'").attr("class", d.labelClass).optionalAttr("href", g).attr(V, e.level).attr(S, e.selected ? "true" : "false").optionalAttr(U, e.disabled ? "true" : null).optionalAttr(R, e.hasChildren === !1 ? null : e.expanded ? "true" : "false").markup(">").content(c.getLabel(b)).markup("</" + h + ">"))
    }
    function k(a) {
        a.tabIndex = 0,
        a.focus()
    }
    function l(a) {
        var b;
        return a.hasClass(M) ? b = a.children("ul").children("li").first() : (b = a.next(),
        0 === b.length && (b = a.parent().parents("li").next("li").first())),
        b
    }
    function m(a) {
        var b;
        return b = a.prev(),
        b.length > 0 ? b.hasClass(M) && (b = b.find("li").filter(":visible").last()) : b = a.parent().parent("li"),
        b
    }
    function n() {
        var a = {};
        window.getSelection ? a = window.getSelection() : document.selection && (a = document.selection.createRange()),
        a.rangeCount ? a.removeAllRanges() : a.text > "" && document.selection.empty()
    }
    function o(a) {
        var b = a.scrollTop()
          , d = a
          , e = null;
        a[0] === document && (d = c(window)),
        d.on("scroll.treeTemp", function() {
            a.scrollTop(b),
            d.off(".treeTemp"),
            clearTimeout(e)
        }),
        e = setTimeout(function() {
            d.off(".treeTemp")
        }, 20)
    }
    function p(a, b, d, e, f) {
        var g = a.val(b).width(d).keydown(function(a) {
            var b = a.which;
            a.shiftKey || a.ctrlKey || a.altKey || (b === $.ENTER ? (e(c(this).val()),
            a.preventDefault()) : b === $.ESCAPE && (setTimeout(function() {
                f()
            }, 10),
            a.preventDefault()))
        }).blur(function(a) {
            e(c(this).val())
        })[0];
        return k(g),
        g.select(),
        g
    }
    var q = "a-TreeView"
      , r = "a-TreeView-node"
      , s = "a-TreeView--noCollapse"
      , t = "." + r
      , u = "a-TreeView-node--topLevel"
      , v = "a-TreeView-row"
      , w = "." + v
      , x = "a-TreeView-content"
      , y = "." + x
      , z = y + ", " + w
      , A = "a-TreeView-label"
      , B = "a-TreeView-toggle"
      , C = "." + B
      , D = "a-TreeView-dragHelper"
      , E = "a-TreeView-placeholder"
      , F = "is-selected"
      , G = "." + F
      , H = "is-disabled"
      , I = "." + H
      , J = "is-focused"
      , K = "is-hover"
      , L = "is-expandable"
      , M = "is-collapsible"
      , N = "is-processing"
      , O = "a-TreeView-node--leaf"
      , P = "a-Icon"
      , Q = "u-RTL"
      , R = "aria-expanded"
      , S = "aria-selected"
      , T = "is-active"
      , U = "aria-disabled"
      , V = "aria-level"
      , W = "<ul role='group'>"
      , X = "</ul>"
      , Y = "selectionChange"
      , Z = "expansionStateChange"
      , $ = c.ui.keyCode;
    c.widget("apex.treeView", c.ui.mouse, {
        version: "5.0",
        widgetEventPrefix: "treeview",
        options: {
            getNodeAdapter: null,
            adapterTypesMap: null,
            showRoot: !0,
            expandRoot: !0,
            collapsibleRoot: !0,
            autoCollapse: !1,
            useLinks: !0,
            multiple: !1,
            idPrefix: null,
            contextMenuAction: null,
            contextMenu: null,
            contextMenuId: null,
            iconType: P,
            labelClass: A,
            doubleClick: !1,
            clickToRename: !1,
            keyboardRename: !1,
            keyboardAdd: !1,
            keyboardDelete: !1,
            tooltip: null,
            navigation: !1,
            dragAndDrop: !1,
            dragMultiple: !1,
            dragReorder: !1,
            dragAppendTo: "parent",
            dragContainment: !1,
            dragCursor: "auto",
            dragCursorAt: !1,
            dragHelper: null,
            dragOpacity: !1,
            dragAnimate: !1,
            dragExpandDelay: 1200,
            dragScroll: !0,
            dragScrollSensitivity: 20,
            dragScrollSpeed: 10,
            dragZIndex: 1e3,
            scope: "default",
            activate: null,
            deactivate: null,
            out: null,
            over: null,
            start: null,
            drag: null,
            beforeStop: null,
            stop: null,
            selectionChange: null,
            expansionStateChange: null,
            activateNode: null,
            beginEdit: null,
            endEdit: null,
            added: null,
            renamed: null,
            deleted: null,
            moved: null,
            copied: null
        },
        scrollTimerId: null,
        delayExpandTimer: null,
        hasCurrent: !1,
        tooltipOptions: null,
        triggerTimerId: null,
        forwardKey: $.RIGHT,
        backwardKey: $.LEFT,
        scrollParent: null,
        animating: !1,
        dragging: !1,
        dragItems: null,
        currentItem: null,
        _create: function() {
            var a = this
              , d = this.element
              , e = this.options;
            if (e.getNodeAdapter || (e.getNodeAdapter = this._parseTreeMarkup(d, e.adapterTypesMap || null)),
            !e.getNodeAdapter)
                throw "Missing required option getNodeAdapter";
            if (this.nodeAdapter = e.getNodeAdapter(),
            this.containerCache = {},
            e.collapsibleRoot === !1 && (e.expandRoot = !0),
            d.addClass(q).attr("role", "tree"),
            this.baseId = (e.idPrefix || d[0].id || "tree") + "_",
            this.labelSelector = "." + e.labelClass,
            e.multiple && d.attr("aria-multiselectable", "true"),
            this.rtlFactor = 1,
            "rtl" === d.css("direction") && (d.addClass(Q),
            this.forwardKey = $.LEFT,
            this.backwardKey = $.RIGHT,
            this.rtlFactor = -1),
            e.disabled && d.attr(U, "true"),
            e.tooltip && this._initTooltips(e.tooltip),
            e.contextMenu)
                if (c.apex.menu) {
                    if (e.contextMenu.menubar)
                        throw "TreeView contextMenu must not be a menubar";
                    e.contextMenu._originalBeforeOpen = e.contextMenu.beforeOpen,
                    e.contextMenu.beforeOpen = function(b, c) {
                        e.contextMenu._originalBeforeOpen && (c.menuElement = a.contextMenu$,
                        c.tree = d,
                        c.treeNodeAdapter = a.nodeAdapter,
                        c.treeSelection = a.getSelection(),
                        c.treeSelectedNodes = a.getNodes(c.treeSelection),
                        e.contextMenu._originalBeforeOpen(b, c))
                    }
                    ,
                    e.contextMenu.oldAfterClose = e.contextMenu.afterClose,
                    e.contextMenu.afterClose = function(b, c) {
                        e.contextMenu.oldAfterClose && (c.menuElement = a.contextMenu$,
                        c.tree = d,
                        e.contextMenu.oldAfterClose(b, c)),
                        c.actionTookFocus || a.focus()
                    }
                    ,
                    this.contextMenu$ = c("<div style='display:none'></div>").appendTo("body"),
                    e.contextMenuId && (this.contextMenu$[0].id = e.contextMenuId),
                    this.contextMenu$.menu(e.contextMenu),
                    e.contextMenuAction && b.warn("TreeView contextMenuAction option ignored when contextMenu option present"),
                    e.contextMenuAction = function(b) {
                        var d, e;
                        "contextmenu" === b.type ? a.contextMenu$.menu("toggle", b.pageX, b.pageY) : (d = c(b.target),
                        e = d.offset(),
                        a.contextMenu$.menu("toggle", e.left, e.top + d.closest(y).height()))
                    }
                } else
                    b.warn("TreeView contextMenu option ignored because menu widget not preset");
            this.scrollParent = d.scrollParent(),
            this.offset = this.element.offset(),
            this._mouseInit(),
            this._on(this._eventHandlers),
            this.renderNodeOptions = {
                iconType: e.iconType,
                labelClass: e.labelClass,
                useLinks: e.useLinks
            },
            this.refresh()
        },
        _eventHandlers: {
            click: function(a) {
                var b, d = this.options, e = c(a.target);
                return d.multiple || "A" !== a.target.nodeName || !a.shiftKey && !a.ctrlKey ? (e.hasClass(B) ? (this._toggleNode(e.parent()),
                this.scrollParent && o(this.scrollParent),
                this.lastFocused.focus(),
                a.preventDefault()) : (b = e.closest(t),
                b.length > 0 && (d.clickToRename && "true" === b.children(y).find(this.labelSelector).attr(S) && !a.ctrlKey && !a.altKey && 1 === this.getSelection().length && e.closest(this.labelSelector).length ? this.renameNodeInPlace(b.children(y)) : (this._select(b.children(y), a, !0),
                d.navigation && (this.keyboardActivate || "activate" !== d.doubleClick) && this._activate(a)),
                a.preventDefault())),
                this.keyboardActivate = !1,
                void n()) : void (this.keyboardActivate = !1)
            },
            dblclick: function(a) {
                var b, d = this.options.doubleClick;
                d && (b = c(a.target).closest(t),
                b.length > 0 && ("toggle" === d ? (this._toggleNode(b),
                a.preventDefault()) : "activate" === d && this._activate(a)))
            },
            keydown: function(a) {
                var b, d, e, f, g, h = this, i = this.options, j = this.element, k = a.which;
                a.altKey || "INPUT" === a.target.nodeName || this.dragging || (k !== $.PAGE_UP && k !== $.PAGE_DOWN || (this.scrollParent ? (e = j.find(w).filter(":visible").first().outerHeight() || 24,
                b = j.find("li").filter(":visible").first(),
                e += parseInt(b.css("margin-top"), 10) + parseInt(b.css("margin-bottom"), 10),
                f = this.scrollParent[0] === document ? c(window).height() : this.scrollParent[0].clientHeight,
                g = Math.floor(f / e) - 1) : g = 10),
                k === $.HOME ? (j.find(y).filter(":visible").first().each(function() {
                    h._select(c(this), a, !0, !0)
                }),
                a.preventDefault()) : k === $.END ? (j.find(y).filter(":visible").last().each(function() {
                    h._select(c(this), a, !0, !0)
                }),
                a.preventDefault()) : k === $.SPACE ? (this.lastFocused && this._select(c(h.lastFocused).closest(y), a, !0, !0),
                a.preventDefault()) : k === $.DOWN ? (this._traverseDown(a, 1),
                a.preventDefault()) : k === $.UP ? (this._traverseUp(a, 1),
                a.preventDefault(),
                a.stopPropagation()) : k === $.PAGE_DOWN ? (this._traverseDown(a, g),
                a.preventDefault()) : k === $.PAGE_UP ? (this._traverseUp(a, g),
                a.preventDefault()) : k === this.backwardKey ? (this.lastFocused && (b = c(this.lastFocused).closest(t),
                b.hasClass(M) ? this._collapseNode(b) : b.parent().prevAll(y).each(function() {
                    h._select(c(this), a, !0, !0)
                })),
                a.preventDefault()) : k === this.forwardKey ? (this.lastFocused && (b = c(this.lastFocused).closest(t),
                b.hasClass(L) ? this._expandNode(b) : b.hasClass(M) && b.children("ul").children("li").first().children(y).each(function() {
                    h._select(c(this), a, !0, !0)
                })),
                a.preventDefault()) : k === $.ENTER ? "A" === a.target.nodeName || a.shiftKey || a.ctrlKey ? this.keyboardActivate = !0 : (this._activate(a),
                a.preventDefault()) : 113 === k && i.keyboardRename ? (d = this.lastFocused && c(this.lastFocused).closest(y + G).length > 0 ? c(this.lastFocused).closest(y) : this.getSelection().first(),
                d.length > 0 && this.renameNodeInPlace(d)) : 45 === k && i.keyboardAdd ? (d = this.lastFocused && c(this.lastFocused).closest(y + G).length > 0 ? c(this.lastFocused).closest(y) : this.getSelection().first(),
                d.length > 0 && this.addNodeInPlace(d)) : k === $.DELETE && i.keyboardDelete ? this.deleteNodes(this.getSelection()) : this.options.contextMenuAction && a.shiftKey && 121 === k && (h.lastFocused && !c(h.lastFocused).closest(y).hasClass(F) && h._select(c(h.lastFocused).closest(y), {}, !1, !0),
                this.options.contextMenuAction(a),
                a.preventDefault()))
            },
            keypress: function(a) {
                function b(a) {
                    function b() {
                        e = l(e),
                        0 === e.length && (e = f.element.find(t).filter(":visible").first())
                    }
                    var d, e, g, h = a.length;
                    for (e = d = c(f.lastFocused).closest(t),
                    1 === h && b(); ; ) {
                        if (g = e.children(y).find(f.labelSelector).first(),
                        g.text().substring(0, h).toLowerCase() === a)
                            return g.closest(y);
                        if (b(),
                        e[0] === d[0])
                            break
                    }
                    return null
                }
                var d, e, f = this;
                if (!(0 === a.which || a.ctrlKey || a.altKey || "INPUT" === a.target.nodeName || this.dragging)) {
                    if (d = String.fromCharCode(a.which).toLowerCase(),
                    this.searchTimerId)
                        d !== this.searchString && (this.searchString += d),
                        clearTimeout(this.searchTimerId),
                        this.searchTimerId = null;
                    else {
                        if (" " === d)
                            return;
                        this.searchString = d
                    }
                    this.searchTimerId = setTimeout(function() {
                        f.searchTimerId = null
                    }, 500),
                    e = b(this.searchString),
                    e && this._select(e, {}, !0, !0)
                }
            },
            focusin: function(a) {
                var b = c(a.target).closest(this.labelSelector);
                b.length && (b.addClass(J).closest(t).children(w).addClass(J),
                this._setFocusable(b))
            },
            focusout: function(a) {
                var b = c(a.target).closest(this.labelSelector);
                b.removeClass(J).closest(t).children(w).removeClass(J)
            },
            mousemove: function(a) {
                var b;
                this.dragging || (b = c(a.target).closest(t),
                b.length && this.lastHover !== b[0] && (c(this.lastHover).children(z).removeClass(K),
                b.children(z).addClass(K),
                this.lastHover = b[0]))
            },
            mouseleave: function(a) {
                this.dragging || this.lastHover && (c(this.lastHover).children(z).removeClass(K),
                this.lastHover = null)
            },
            contextmenu: function(a) {
                var b;
                this.options.contextMenuAction && (b = c(a.target).closest(y).not(G),
                b.length && this._select(b, {}, !1, !1),
                this.options.contextMenuAction(a),
                a.preventDefault())
            }
        },
        _setOption: function(a, d) {
            var e;
            if ("disabled" === a)
                this.options[a] = d,
                this.widget().toggleClass(H, !!d),
                d ? (this.element.attr(U, "true"),
                this.lastFocused && (this.lastFocused.tabIndex = -1),
                this.lastFocused = null) : (this.element.removeAttr(U),
                e = this.getSelection().first().find(this.labelSelector),
                e.length || (e = this.element.find(this.labelSelector).first()),
                this._setFocusable(e));
            else {
                if ("contextMenu" === a || "contextMenuId" === a)
                    throw "TreeView " + a + " cannot be set";
                if ("contextMenuAction" === a && this.options.contextMenu)
                    throw "TreeView contextMenuAction cannot be set when the contextMenu option is used";
                if ("dragMultiple" === a && d && !this.options.multiple)
                    throw "TreeView dragMultiple cannot be true when the multiple option is false";
                if ("multiple" === a && !d && this.options.dragMultiple)
                    throw "TreeView multiple cannot be false when the dragMultiple option is true";
                if ("collapsibleRoot" === a)
                    throw "TreeView collapsibleRoot option cannot be set";
                c.Widget.prototype._setOption.apply(this, arguments)
            }
            this.renderNodeOptions = {
                iconType: this.options.iconType,
                labelClass: this.options.labelClass,
                useLinks: this.options.useLinks
            },
            "showRoot" === a || "useLinks" === a ? this.refresh() : "getNodeAdapter" === a ? (this.nodeAdapter = this.options.getNodeAdapter(),
            this.refresh()) : "multiple" === a ? (this.element.attr("aria-multiselectable", d ? "true" : "false"),
            d === !1 && this.getSelection().length > 0 && this._select(c(this.lastFocused).closest(y), {}, !1, !1)) : "expandRoot" === a && d === !1 ? this.options.collapsibleRoot === !1 && (this.options.expandRoot = !0,
            b.warn("ExpandRoot option cannot be false when collapsibleRoot is false")) : "tooltip" === a && this._initTooltips(d)
        },
        _initTooltips: function(a) {
            var d, e = this;
            return c.ui.tooltip ? (this.tooltipOptions && (this.element.tooltip("destroy"),
            this.tooltipOptions = null),
            void (a && (d = this.tooltipOptions = c.extend(!0, {}, a),
            d.items = this.labelSelector,
            d.content && c.isFunction(d.content) && (d._originalContent = d.content,
            d.content = function(a) {
                var b = e.getNodes(c(this).closest(y))[0];
                return d._originalContent.call(this, a, b)
            }
            ),
            this.element.tooltip(d)))) : void b.warn("tooltip option ignored because missing tooltip widget dependency")
        },
        _destroy: function() {
            this.element.empty().removeClass(q + " " + Q).removeAttr("role").removeAttr("aria-multiselectable"),
            this.contextMenu$ && this.contextMenu$.remove(),
            this.options.tooltip && c.ui.tooltip && this.element.tooltip("destroy"),
            this._mouseDestroy()
        },
        refresh: function(b) {
            var d, e, f, i = this, j = this.options, k = this.nodeAdapter, l = null, m = this.element, n = a.htmlBuilder();
            k.getViewId && (l = this.getSelectedNodes()),
            b ? b.each(function() {
                var a = c(this).parent()
                  , b = i.treeMap[g(a)];
                a.find(t).addBack().each(function() {
                    delete i.treeMap[g(c(this))]
                }),
                n.clear(),
                i._renderNode(b, h(a, i.labelSelector), n),
                a.replaceWith(n.toString())
            }) : (this.treeMap = {},
            this.nextNodeId = 0,
            k.clearViewId && k.clearViewId(this.baseId),
            d = k.root(),
            d ? (n.markup(W),
            j.showRoot ? this._renderNode(d, 1, n) : k.hasChildren(d) && this._renderChildren(d, 1, n),
            n.markup(X),
            m.html(n.toString())) : (n.markup(W),
            n.markup(X),
            m.html(n.toString())),
            j.expandRoot && j.showRoot && (e = this._getRoots(),
            e.length > 0 && this._expandNode(e))),
            this.hasCurrent ? (f = this.find({
                depth: -1,
                match: function(a) {
                    return a.current === !0
                }
            }),
            this.hasCurrent = !1,
            this.setSelection(f)) : l && l.length > 0 ? this.setSelectedNodes(l) : (this.selectAnchor = this.lastFocused,
            this._setFocusable(m.find(this.labelSelector).first()))
        },
        getNodeAdapter: function() {
            return this.nodeAdapter
        },
        focus: function() {
            this.lastFocused && this.lastFocused.focus()
        },
        getTreeNode: function(a) {
            var b, d = this.nodeAdapter;
            if (!d.getViewId)
                throw "Unsupported by model";
            return b = d.getViewId(this.baseId, a),
            c("#" + this.baseId + b).children(y)
        },
        getSelection: function() {
            return this.element.find(y + G)
        },
        getNodes: function(a) {
            var b = this
              , d = [];
            return a.each(function() {
                d.push(b.treeMap[g(c(this).closest("li"))])
            }),
            d
        },
        getSelectedNodes: function() {
            return this.getNodes(this.getSelection())
        },
        setSelection: function(a, b) {
            b = !!b,
            this.options.multiple || (a = a.first()),
            this._select(a, null, b, !1)
        },
        setSelectedNodes: function(a, d) {
            var e, f, g, h = [], i = this.nodeAdapter;
            if (!i.getViewId)
                throw "Unsupported by model";
            for (d = !!d,
            this.options.multiple || (a = [a[0]]),
            e = 0; e < a.length; e++)
                f = i.getViewId(this.baseId, a[e]),
                g = c("#" + this.baseId + f).children(y)[0],
                g ? h.push(g) : b.warn("TreeView: Ignoring bad node in setSelectedNodes");
            this._select(c(h), null, d, !1, !0)
        },
        getExpandedNodeIds: function() {
            var a = this.nodeAdapter;
            if (!a.getExpandedNodeIds)
                throw "Unsupported by model";
            return a.getExpandedNodeIds(this.baseId)
        },
        getExpandedState: function() {
            var a = this.nodeAdapter;
            if (!a.getExpandedState)
                throw "Unsupported by model";
            return a.getExpandedState(this.baseId)
        },
        find: function(a) {
            return c(this._find(a.parentNodeContent$ || null, a.match, a.depth || 1, a.findAll || !1))
        },
        expand: function(a) {
            var b = this;
            a || (a = this._getRoots().children(y)),
            a.each(function() {
                var a = c(this).closest(t);
                a.hasClass(L) && b._expandNode(a)
            })
        },
        expandAll: function(a) {
            var b = this;
            a || (a = this._getRoots().children(y)),
            a.each(function() {
                var a = c(this).closest(t);
                a.hasClass(L) ? b._expandNode(a, function() {
                    b.expandAll(a.children("ul").children("li").children(y))
                }) : b.expandAll(a.children("ul").children("li").children(y))
            })
        },
        collapse: function(a) {
            var b = this;
            a || (a = this._getRoots().children(y)),
            a.each(function() {
                var a = c(this).closest(t);
                a.hasClass(M) && b._collapseNode(a)
            })
        },
        collapseAll: function(a) {
            var b = this;
            a || (a = this._getRoots().children(y)),
            a.each(function() {
                var a = c(this).closest(t);
                b.collapseAll(a.children("ul").children("li").children(y)),
                a.hasClass(M) && b._collapseNode(a)
            })
        },
        addNodeInPlace: function(b, c, e) {
            function f() {
                m.remove(),
                q._makeLeafIfNeeded(b),
                q._select(b, {}, !0),
                q._endEdit({
                    action: "add",
                    status: "cancel"
                })
            }
            function h(d) {
                var g;
                w || (w = !0,
                u.addNode(n, l.children().length - 1, d, e, function(d, e) {
                    var h, i;
                    return d === !1 ? (w = !1,
                    g = m.find("input").val(c).get(0),
                    k(g),
                    void g.select()) : void (d ? (m.remove(),
                    i = a.htmlBuilder(),
                    q._renderNode(d, o, i),
                    e >= l.children("li").length ? l.append(i.toString()) : l.children("li").eq(e).before(i.toString()),
                    h = l.children("li").eq(e),
                    q._select(h.children(y), {}, !0),
                    q._endEdit({
                        action: "add",
                        status: "complete"
                    }),
                    q._trigger("added", {}, {
                        parentNode: n,
                        parent$: b,
                        index: e,
                        node: d,
                        node$: h.children(y)
                    })) : f())
                }))
            }
            function j() {
                var b, d, g, i = a.htmlBuilder(), j = q.baseId + "new";
                i.markup("<li").attr("id", j).attr("class", r + " " + O).markup("><div").attr("class", v).markup("></div><div").attr("class", x).markup(">"),
                u.getIcon && i.markup("<span").attr("class", t.iconType).markup("></span>"),
                i.markup("<span role='treeitem'").attr("class", t.labelClass).attr(V, o).attr(S, "true").markup("><input type='text'></span></div></li>"),
                l.append(i.toString()),
                m = l.find("#" + j),
                d = m.children(y),
                b = 1 === q.rtlFactor ? d.width() - d.find(q.labelSelector)[0].offsetLeft - 16 : d.find(q.labelSelector)[0].offsetLeft + d.find(q.labelSelector).width() - 16,
                g = d.find("input"),
                p(g, c, b, h, f),
                q._beginEdit({
                    action: "add",
                    context: e,
                    input: g[0]
                })
            }
            var l, m, n, o, q = this, s = this.element, t = this.options, u = this.nodeAdapter, w = !1;
            if (!u.addNode || !u.allowAdd)
                throw "Unsupported by model";
            if (null === b) {
                if (n = u.root(),
                !t.showRoot) {
                    if (!u.allowAdd(n, "add", e ? [e] : d))
                        return;
                    return o = 1,
                    l = s.find("ul:first"),
                    void j()
                }
                b = s.find("ul:first > li")
            } else
                n = this.treeMap[g(b.parent())];
            u.allowAdd(n, "add", e ? [e] : d) && (o = i(b, q.labelSelector) + 1,
            q._makeParentIfNeeded(b),
            this._expandNode(b.parent(), function() {
                l = b.next("ul"),
                j()
            }))
        },
        renameNodeInPlace: function(b) {
            function c() {
                u.clear(),
                j(u, f, q, o.renderNodeOptions, n),
                b.html(u.toString()),
                o._select(b, {}, !0),
                o._endEdit({
                    action: "rename",
                    status: "cancel"
                })
            }
            function e(a) {
                var d;
                if (!t)
                    return t = !0,
                    a === i ? void c() : void q.renameNode(f, a, function(a, e) {
                        var f, g, h;
                        return a === !1 ? (t = !1,
                        d = b.find("input").val(i)[0],
                        k(d),
                        void d.select()) : void (a ? (u.clear(),
                        j(u, a, q, o.renderNodeOptions, n),
                        b.html(u.toString()),
                        o.treeMap[s] = a,
                        g = r.parent(),
                        h = g.children("li"),
                        f = h.index(r),
                        f !== e && (e > f && (e += 1),
                        e >= h.length ? g.append(r) : h.eq(e).before(r)),
                        o._select(b, {}, !0),
                        o._endEdit({
                            action: "rename",
                            status: "complete"
                        }),
                        o._trigger("renamed", {}, {
                            prevLabel: i,
                            index: e,
                            node: a,
                            node$: b
                        }),
                        o._trigger(Y, 0)) : c())
                    })
            }
            var f, h, i, l, m, n, o = this, q = (this.options,
            this.nodeAdapter), r = b.parent(), s = g(r), t = !1, u = a.htmlBuilder();
            if (!q.renameNode || !q.allowRename)
                throw "Unsupported by model";
            f = this.treeMap[s],
            q.allowRename(f) && (m = b.find(this.labelSelector),
            n = {
                level: parseInt(m.attr(V), 10),
                selected: "true" === m.attr(S),
                disabled: "true" === m.attr(U),
                hasChildren: m.attr(R) !== d,
                expanded: "true" === m.attr(R)
            },
            i = q.getLabel(f),
            l = 1 === o.rtlFactor ? b.width() - m[0].offsetLeft - 16 : m[0].offsetLeft + m.width() - 16,
            m.html("<input type='text'>"),
            h = b.find("input"),
            p(h, i, l, e, c),
            o._beginEdit({
                action: "rename",
                node: f,
                input: h[0]
            }))
        },
        deleteNodes: function(a) {
            function b(a) {
                function b(a) {
                    h += 1,
                    a && (k.push(d.element),
                    l.push({
                        node: d.node,
                        parent$: d.parent$,
                        index: d.index
                    }),
                    m.clearViewId && m.clearViewId(i.baseId, d.node)),
                    h >= e && (i.deleteTreeNodes(c(k)),
                    i._trigger("deleted", {}, {
                        items: l
                    }))
                }
                var d = j[a];
                m.deleteNode(d.node, b, a < e - 1)
            }
            var d, e, h, i = this, j = [], k = [], l = [], m = this.nodeAdapter;
            if (!m.deleteNode || !m.allowDelete)
                throw "Unsupported by model";
            for (a.each(function() {
                var a = c(this)
                  , b = i.treeMap[g(a.parent())];
                m.allowDelete(b) && j.push({
                    node: b,
                    element: a[0],
                    parent$: a.parent().parent().parent().children(y),
                    index: f(a.parent())
                })
            }),
            e = j.length,
            h = 0,
            d = 0; d < e; d++)
                b(d)
        },
        deleteTreeNodes: function(a) {
            var b, c = this, d = a.closest("ul").prev(), e = a.parent(), f = a.children(this.labelSelector).filter(this.lastFocused).length > 0, h = a.hasClass(F);
            (h || f) && (b = m(e.eq(0)),
            0 === b.length && (b = this._getRoots().first()),
            b.length > 0 ? h ? this._select(b.children(y), {}, f) : this._setFocusable(b.children(y).find(this.labelSelector)) : f && (this.lastFocused = null)),
            e.remove().each(function() {
                delete c.treeMap[g(e)]
            }),
            this._makeLeafIfNeeded(d)
        },
        addNode: function(a, b, c) {
            var e, f, h = this.nodeAdapter;
            if (!h.addNode || !h.allowAdd)
                throw "Unsupported by model";
            if (a && a.length)
                f = this.treeMap[g(a.parent())];
            else {
                if (this.options.showRoot)
                    throw "Parent node required";
                f = h.root()
            }
            h.allowAdd(f, "add", c ? [c] : d) && (e = this.element.find("." + J).length > 0,
            this._add({}, a, b, c, e))
        },
        moveNodes: function(a, b, c) {
            var d, e, f, h = this.getNodes(c), i = !0, j = this.nodeAdapter;
            if (!j.moveNodes || !j.allowDelete || !j.allowAdd)
                throw "Unsupported by model";
            if (a && a.length)
                f = this.treeMap[g(a.parent())];
            else {
                if (this.options.showRoot)
                    throw "Parent node required";
                f = j.root()
            }
            for (d = 0; d < h.length; d++)
                if (!j.allowDelete(h[d])) {
                    i = !1;
                    break
                }
            i && j.allowAdd(f, "move", h) && (e = this.element.find("." + J).length > 0,
            this._moveOrCopy({}, a, b, c, !1, e))
        },
        copyNodes: function(a, b, c) {
            var d, e, f = this.getNodes(c), h = this.nodeAdapter;
            if (!h.copyNodes || !h.allowAdd)
                throw "Unsupported by model";
            if (a && a.length)
                e = this.treeMap[g(a.parent())];
            else {
                if (this.options.showRoot)
                    throw "Parent node required";
                e = h.root()
            }
            h.allowAdd(e, "copy", f) && (d = this.element.find("." + J).length > 0,
            this._moveOrCopy({}, a, b, c, !0, d))
        },
        update: function(b) {
            var c, f, h, i, k, l, m = this.treeMap[g(b.parent())], n = this.nodeAdapter, o = a.htmlBuilder();
            i = b.find(this.labelSelector),
            c = i[0] === this.lastFocused,
            (n.getClasses || n.isDisabled) && (h = b.prevAll(w),
            e(b[0], [x, H, J, F, K]),
            e(h[0], [v, H, J, F, K]),
            n.getClasses && (f = n.getClasses(m),
            f && (b.addClass(f),
            h.addClass(f))),
            n.isDisabled && n.isDisabled(m) && (b.addClass(H),
            h.addClass(H),
            l = !0)),
            k = {
                level: parseInt(i.attr(V), 10),
                selected: "true" === i.attr(S),
                disabled: l,
                hasChildren: i.attr(R) !== d,
                expanded: "true" === i.attr(R)
            },
            j(o, m, n, this.renderNodeOptions, k),
            b.html(o.toString()),
            c && this._setFocusable(b.find(this.labelSelector))
        },
        _parseTreeMarkup: function(a, b) {
            function d(a) {
                var b = [];
                return a.children("ul").children("li").each(function() {
                    var a, e, f, g, j, k = c(this), l = k.children("a").first(), m = k.children("span").first();
                    a = {},
                    l.length > 0 ? (a.label = l.text(),
                    a.link = l.attr("href")) : m.length > 0 && (a.label = m.text()),
                    f = k.attr("data-id"),
                    f ? a.id = f : h = !1,
                    "true" === k.attr("data-current") && (a.current = !0,
                    i.hasCurrent = !0),
                    g = k.attr("class"),
                    g && (a.classes = g),
                    "true" === k.attr("data-disabled") && (a.isDisabled = !0),
                    e = k.attr("data-icon"),
                    e && (a.icon = e),
                    j = k.attr("data-type"),
                    j && (a.type = j),
                    k.children("ul").length > 0 && (a.children = d(k)),
                    b.push(a)
                }),
                b
            }
            var e, f, g, h = !0, i = this;
            return f = d(a),
            g = f.length >= 1 ? 1 === f.length && this.options.showRoot ? f[0] : {
                children: f
            } : null,
            b || (b = {
                "default": {
                    operations: {
                        canAdd: !1,
                        canDelete: !1,
                        canRename: !1,
                        canDrag: !1
                    }
                }
            }),
            e = c.apex.treeView.makeDefaultNodeAdapter(g, b, h),
            function() {
                return e
            }
        },
        _renderNode: function(a, b, c) {
            var d, e, f, g, h, i, k, l, m = !1, n = this.options, o = this.nodeAdapter;
            e = this.nextNodeId,
            this.treeMap[e] = a,
            o.setViewId && o.setViewId(this.baseId, a, e),
            this.nextNodeId += 1,
            f = r + " ",
            d = o.hasChildren(a),
            null === d && (d = !0),
            d ? (i = !1,
            o.isExpanded && (i = o.isExpanded(this.baseId, a)),
            f += i ? M : L) : f += O,
            h = 0 === e && n.showRoot && !n.collapsibleRoot,
            h && (f += " " + s),
            1 === b && (f += " " + u),
            g = x,
            o.isDisabled && o.isDisabled(a) && (g += " " + H,
            m = !0),
            k = v,
            c.markup("<li").attr("id", this.baseId + e).attr("class", f).markup(">"),
            o.getClasses && (l = o.getClasses(a),
            l && (g += " " + l,
            k += " " + l)),
            c.markup("<div").attr("class", k).markup("></div>"),
            d && !h && c.markup("<span class='" + B + "'></span>"),
            c.markup("<div").attr("class", g).markup(">"),
            j(c, a, o, this.renderNodeOptions, {
                level: b,
                selected: !1,
                disabled: m,
                hasChildren: d,
                expanded: i
            }),
            c.markup("</div>"),
            i && (c.markup(W),
            this._renderChildren(a, b + 1, c),
            c.markup(X)),
            c.markup("</li>")
        },
        _renderChildren: function(b, c, d, e, f) {
            function g() {
                var a;
                for (a = 0; a < h; a++)
                    i._renderNode(j.child(b, a), c, d);
                e && e(!0)
            }
            var h, i = this, j = this.nodeAdapter;
            h = j.childCount(b),
            null === h ? e && (a.delayLinger.start(f[0].id, function() {
                f.addClass(N)
            }),
            j.fetchChildNodes(b, function(c) {
                if (a.delayLinger.finish(f[0].id, function() {
                    f.removeClass(N),
                    0 === c && e(c)
                }),
                c) {
                    if (h = j.childCount(b),
                    h > 0)
                        return void g();
                    c = 0
                }
                c === !1 && e(c)
            })) : h > 0 ? g() : e && e(0)
        },
        _getRoots: function() {
            return this.element.children("ul").children("li")
        },
        _find: function(a, b, d, e) {
            var f, h, i, j = this, k = [];
            return a ? (i = a.parent(),
            this._addChildrenIfNeeded(i),
            h = i.children("ul").children("li")) : h = this._getRoots(),
            h.each(function() {
                if (f = j.treeMap[g(c(this))],
                b(f) && (k.push(c(this).children(y)[0]),
                !e))
                    return !1
            }),
            (e || 0 === k.length) && (d > 1 || d === -1) && h.each(function() {
                if (k = k.concat(j._find(c(this).children(y), b, d === -1 ? d : d - 1, e)),
                k.length > 0 && !e)
                    return !1
            }),
            k
        },
        _makeParentIfNeeded: function(a) {
            a && 0 === a.prev(C).length && (a.parent().removeClass(O).addClass(L),
            a.before("<span class='" + B + "'></span>"),
            a.after(W + X),
            a.parent().children("ul").hide())
        },
        _makeLeafIfNeeded: function(a) {
            var b = this
              , d = this.nodeAdapter;
            a.each(function() {
                var a, e, f = c(this);
                0 === f.next("ul").find("li").length && (e = f.parent(),
                e.hasClass(M) && d.setExpanded && (a = b.treeMap[g(e)],
                d.setExpanded(b.baseId, a, !1)),
                f.parent().removeClass(L + " " + M).addClass(O),
                f.find(b.labelSelector).removeAttr(R),
                f.prev(C).remove(),
                f.next("ul").remove())
            })
        },
        _addChildrenIfNeeded: function(b) {
            var c, d, e = this.treeMap[g(b)];
            c = b.children("ul"),
            c.length > 0 || b.hasClass(O) || (d = a.htmlBuilder(),
            d.markup(W),
            this._renderChildren(e, h(b, this.labelSelector) + 1, d),
            d.markup(X),
            b.append(d.toString()).children("ul").hide())
        },
        _toggleNode: function(a) {
            a.hasClass(L) ? this._expandNode(a) : this._collapseNode(a)
        },
        _persistExpansionState: function(a, b, c) {
            var d = this.nodeAdapter;
            d.setExpanded && d.setExpanded(this.baseId, a, c),
            this._trigger(Z, {}, {
                node: a,
                nodeContent$: b.children(y),
                expanded: c
            })
        },
        _expandNode: function(b, d) {
            var e, f, i = this, j = this.nodeAdapter, k = this.treeMap[g(b)];
            this.options.autoCollapse && b.parent().children("." + M).each(function() {
                i._collapseNode(c(this))
            }),
            b.removeClass(L),
            e = b.children("ul"),
            e.length > 0 && null !== j.childCount(k) ? (e.show(),
            b.addClass(M).children(y).find(this.labelSelector).attr(R, "true"),
            this._persistExpansionState(k, b, !0),
            d && d()) : (e.remove(),
            f = a.htmlBuilder(),
            f.markup(W),
            this._renderChildren(k, h(b, this.labelSelector) + 1, f, function(a) {
                a ? (b.addClass(M).children(y).find(i.labelSelector).attr(R, "true"),
                f.markup(X),
                b.append(f.toString()),
                i._persistExpansionState(k, b, !0)) : 0 === a ? (b.children(C).remove(),
                b.addClass(O).children(y).find(i.labelSelector).removeAttr(R)) : (b.addClass(L).children(y).find(i.labelSelector).attr(R, "false"),
                i._persistExpansionState(k, b, !1)),
                d && d()
            }, b))
        },
        _collapseNode: function(a) {
            var b = this.options;
            b.showRoot && !b.collapsibleRoot && a.parent().parent().hasClass(q) || (a.removeClass(M).addClass(L).children(y).find(this.labelSelector).attr(R, "false"),
            a.find(G).length > 0 && this._select(a.children(y), {}, !0),
            a.children("ul").hide(),
            this._persistExpansionState(this.treeMap[g(a)], a, !1))
        },
        _traverseDown: function(a, b) {
            var d, e, f;
            if (this.lastFocused) {
                for (d = c(this.lastFocused).closest(t),
                f = 0; f < b && (e = l(d),
                0 !== e.length); f++)
                    d = e;
                d.length > 0 && this._select(d.children(y), a, !0, !0)
            }
        },
        _traverseUp: function(a, b) {
            var d, e, f;
            if (this.lastFocused) {
                for (d = c(this.lastFocused).closest(t),
                f = 0; f < b && (e = m(d),
                0 !== e.length); f++)
                    d = e;
                d.length > 0 && this._select(d.children(y), a, !0, !0)
            }
        },
        _activate: function(a) {
            var b, c = this.options, d = this.nodeAdapter, e = this.getSelectedNodes();
            0 !== e.length && (this._trigger("activateNode", a, {
                nodes: e
            }),
            c.navigation && d.getLink && !a.isDefaultPrevented() && (b = d.getLink(e[0]),
            b && apex.navigation.redirect(b)))
        },
        _select: function(a, b, d, e, f) {
            var g, h, i, j, m, n, o, p, q = a, r = "set", s = this, u = this.element.find(y + G);
            if (b && this.options.multiple && ("click" === b.type ? b.ctrlKey || b.metaKey ? r = "toggle" : b.shiftKey && (r = "range") : "keydown" === b.type && (b.keyCode === c.ui.keyCode.SPACE ? r = b.ctrlKey ? "toggle" : b.shiftKey ? "range" : "add" : b.ctrlKey ? r = "none" : b.shiftKey && (r = "range"))),
            "range" !== r || this.selectAnchor || (r = "set"),
            "set" !== r && "range" !== r || (u.prevAll(w).addBack().removeClass(F),
            u.find(this.labelSelector).attr(S, "false")),
            h = a.eq(0).find(this.labelSelector),
            a = a.not(I),
            j = a.hasClass(F),
            "set" === r || "add" === r || "toggle" === r && !j)
                a.prevAll(w).addBack().addClass(F),
                a.find(this.labelSelector).attr(S, "true"),
                a.parent().parents(t).each(function() {
                    g = c(this),
                    g.hasClass(L) && s._expandNode(g)
                }),
                this.selectAnchor = a[0];
            else if ("range" === r) {
                for (i = c("#" + this.selectAnchor.parentNode.id + ", #" + q[0].parentNode.id),
                g = i.first(); ; )
                    if (g.children(y).hasClass(H) || (g.children(y).prevAll(w).addBack().addClass(F),
                    g.children(y).find(this.labelSelector).attr(S, "true")),
                    g = l(g),
                    0 === g.length || 1 === i.length || g[0] === i[1])
                        break;
                g.length > 0 && 2 === i.length && !g.children(y).hasClass(H) && (g.children(y).prevAll(w).addBack().addClass(F),
                g.children(y).find(this.labelSelector).attr(S, "true"))
            } else
                "toggle" === r && j && (a.prevAll(w).addBack().removeClass(F),
                a.find(this.labelSelector).attr(S, "false"),
                this.selectAnchor = a[0]);
            h.length > 0 && (d ? k(h[0]) : this._setFocusable(h),
            this.scrollParent && (m = this.scrollParent[0],
            p = h.parent().offset(),
            o = this.element.offset(),
            m === document ? (n = {
                top: c(document).scrollTop(),
                left: c(document).scrollLeft()
            },
            (p.top < n.top || p.top > n.top + c(window).height()) && c(document).scrollTop(p.top - o.top),
            (p.left + h.parent()[0].offsetWidth < n.left || p.left > n.left + c(window).width()) && c(document).scrollLeft(p.left - o.left)) : (n = this.scrollParent.offset(),
            o = this.element.offset(),
            (p.top < n.top || p.top > n.top + m.offsetHeight) && (m.scrollTop = p.top - o.top),
            (p.left + h.parent()[0].offsetWidth < n.left || p.left > n.left + m.offsetWidth) && (m.scrollLeft = p.left - o.left)))),
            f || ("toggle" === r || "range" === r && !j || "add" === r && !j || "set" === r && (u[0] !== a[0] || u.length !== a.length)) && (s.triggerTimerId && (clearTimeout(s.triggerTimerId),
            s.triggerTimerId = null),
            s.triggerTimerId = setTimeout(function() {
                s.triggerTimerId = null,
                s._trigger(Y, b)
            }, e ? 350 : 1))
        },
        _setFocusable: function(a) {
            var b = a[0];
            b && (this.lastFocused && this.lastFocused !== b && (this.lastFocused.tabIndex = -1),
            b.tabIndex = 0,
            this.lastFocused = b)
        },
        _beginEdit: function(a) {
            apex.tooltipManager && apex.tooltipManager.disableTooltips(),
            this._trigger("beginEdit", {}, a)
        },
        _endEdit: function(a) {
            apex.tooltipManager && apex.tooltipManager.enableTooltips(),
            this._trigger("endEdit", {}, a)
        },
        _mouseCapture: function(a, b) {
            var d, e, f, g = !0, h = this.options;
            if (a.preventDefault(),
            this.animating || h.disabled || !h.dragAndDrop || c(a.target).hasClass(B))
                return !1;
            if (e = c(a.target).closest(t).children(y),
            0 === e.length)
                return !1;
            if (h.dragMultiple && (e.hasClass(F) ? e = this.getSelection() : a.ctrlKey && (e = e.add(this.getSelection()))),
            b !== !0) {
                for (f = this.getNodes(e),
                d = 0; d < f.length; d++)
                    if (!this.nodeAdapter.allowDrag || !this.nodeAdapter.allowDrag(f[d])) {
                        g = !1;
                        break
                    }
                if (!g)
                    return !1
            }
            return this.dragItems = e,
            !0
        },
        _mouseStart: function(a, b, d) {
            var e, f, g = null, h = this.options, i = this;
            return d || (c("body").on("keydown.treeview", function(a) {
                return a.keyCode === c.ui.keyCode.ESCAPE ? void i._cancel(a) : void i._dragCopyOrMove(a, !0)
            }),
            c("body").on("keyup.treeview", function(a) {
                i._dragCopyOrMove(a, !0)
            }),
            this._select(this.dragItems, {}, !0, !1)),
            this.helper || (this.helper = this._createHelper(b)),
            this.margins = {
                left: parseInt(this.dragItems.css("marginLeft"), 10) || 0,
                top: parseInt(this.dragItems.css("marginTop"), 10) || 0
            },
            this.offset = this.dragItems.offset(),
            this.offset = {
                top: this.offset.top - this.margins.top,
                left: this.offset.left - this.margins.left
            },
            c.extend(this.offset, {
                click: {
                    left: b.pageX - this.offset.left,
                    top: b.pageY - this.offset.top
                },
                parent: this._getParentOffset()
            }),
            this.helper.css("position", "absolute"),
            this._cacheHelperProportions(),
            c.ui.ddmanager && !d && (this.currentItem = this.dragItems.first(),
            c.ui.ddmanager.current = this,
            c.ui.ddmanager.prepareOffsets(this, a)),
            this.originalPosition = this._generatePosition(b),
            h.dragCursorAt && this._adjustOffsetFromHelper(h.dragCursorAt),
            this.dragItems && this.dragItems.length > 0 && !this.isOver && (g = this.getNodes(this.dragItems),
            g[0] || (g = null)),
            this.nodeAdapter.dragOperations ? this.dragOperations = this.nodeAdapter.dragOperations(g) : this.dragOperations = g ? {
                normal: "move",
                ctrl: "copy"
            } : {
                normal: "add"
            },
            this.dragOperation = this.dragOperations.normal,
            this.dragging = !0,
            this.lastHover && (c(this.lastHover).children(z).removeClass(K),
            this.lastHover = null),
            h.dragReorder && (f = this.dragItems.first().outerHeight(),
            "move" === this.dragOperation && this.dragItems.parent().hide(),
            this._createPlaceholder(f),
            this.initialPlaceholderPos = null),
            this._initPositions(),
            this._refreshPositions(),
            h.dragContainment && this._setContainment(),
            d || h.dragCursor && "auto" !== h.dragCursor && (e = this.document.find("body"),
            this.storedCursor = e.css("cursor"),
            e.css("cursor", h.dragCursor),
            this.storedStylesheet = c("<style>*{ cursor: " + h.dragCursor + " !important; }</style>").appendTo(e)),
            h.dragOpacity && this.helper.css("opacity", h.dragOpacity),
            h.dragZIndex && this.helper.css("zIndex", h.dragZIndex),
            this.helper.addClass(D),
            this.scrollParent && this.scrollParent[0] !== document && "HTML" !== this.scrollParent[0].tagName && (this.overflowOffset = this.scrollParent.offset(),
            this.originalScroll = {
                top: this.scrollParent[0].scrollTop,
                left: this.scrollParent[0].scrollLeft
            }),
            apex.tooltipManager && apex.tooltipManager.disableTooltips(),
            this._trigger("start", b, this._uiHashDnD()),
            this._mouseDrag(b),
            c.ui.ddmanager && !d && c.ui.ddmanager.dragStart(this, b),
            !0
        },
        _mouseDrag: function(a) {
            var b = {
                pageX: a.pageX,
                pageY: a.pageY
            };
            return this.position = this._generatePosition(a),
            this.positionAbs = this._adjustPositionForScroll(),
            this.lastPositionAbs || (this.lastPositionAbs = this.positionAbs),
            this.dragEventTarget = a.target,
            this.options.dragScroll && (this._scrollCheck(b) ? this.scrollTimerId || this._scrollStart(b) : this.scrollTimerId && this._scrollStop()),
            this.helper[0].style.left = this.position.left + "px",
            this.helper[0].style.top = this.position.top + "px",
            this._dragCopyOrMove(a),
            this._dragHitCheck(),
            c.ui.ddmanager && !this.isOver && c.ui.ddmanager.drag(this, a),
            this._trigger("drag", a, this._uiHashDnD()),
            this.lastPositionAbs = this.positionAbs,
            !1
        },
        _dragHitCheck: function() {
            function a() {
                var a = l.positionAbs.top - l.lastPositionAbs.top;
                return 0 !== a && (a > 0 ? "down" : "up")
            }
            function b() {
                l.delayExpandTimer && (clearTimeout(l.delayExpandTimer),
                l.delayExpandTimer = null)
            }
            var d, e, f, g, h, i, j, k, l = this, m = 0, n = null, o = this.dropTargetNode ? this.dropTargetNode[0].id : null, p = this.options;
            if (this.scrollParent[0] !== document && (m = this.scrollParent[0].scrollTop - this.dropPositionsOrigin),
            f = this.positionAbs.left + this.offset.click.left,
            f > this.containerCache.left && f < this.containerCache.left + this.containerCache.width)
                if (this.placeholder && c(this.dragEventTarget).closest("." + E).length)
                    null === this.initialPlaceholderPos && (this.initialPlaceholderPos = f),
                    k = (f - this.initialPlaceholderPos) * this.rtlFactor,
                    k > (this.options.dragScrollSensitivity || 10) ? (this.initialPlaceholderPos = f,
                    this._movePlaceholder({
                        element: this.placeholder.children(y)
                    }, "below")) : k < (-this.options.dragScrollSensitivity || -10) && (this.initialPlaceholderPos = f,
                    this._movePlaceholder({
                        element: this.placeholder.children(y)
                    }, "above"));
                else
                    for (this.initialPlaceholderPos = null,
                    g = this.positionAbs.top + this.offset.click.top + m,
                    d = 0; d < this.dropPositions.length; d++)
                        if (e = this.dropPositions[d],
                        g >= e.top && g <= e.bottom) {
                            n = e.nodeId,
                            i = g > e.top + (e.bottom - e.top) / 2 ? "bottom" : "top";
                            break
                        }
            o === n && i === this.lastLocation || (b(),
            this.element.find("." + T).removeClass(T),
            n ? (h = c("#" + n),
            p.dragExpandDelay >= 0 && h.hasClass(L) && (this.delayExpandTimer = setTimeout(function() {
                l.delayExpandTimer = null,
                l._expandNode(h, function() {
                    l._initPositions(h),
                    l._refreshPositions()
                })
            }, p.dragExpandDelay)),
            e.canAdd ? (this.dropTargetNode = h,
            this.placeholder ? (j = a(),
            "top" === i && "up" === j ? this._movePlaceholder(e, "before") : "bottom" === i && "down" === j && this._movePlaceholder(e, "after")) : this.dropTargetNode.children(y + "," + w).addClass(T)) : e.canAddChild && this.placeholder && (this.initialPlaceholderPos = f,
            this._movePlaceholder(e, "after"),
            this._movePlaceholder({
                element: this.placeholder.children(y)
            }, "below"))) : this.dropTargetNode = null),
            this.lastLocation = i
        },
        _mouseStop: function(a, b) {
            var d, e, f = this;
            return this.delayExpandTimer && (clearTimeout(this.delayExpandTimer),
            this.delayExpandTimer = null),
            this._scrollStop(),
            c.ui.ddmanager && !b && c.ui.ddmanager.dragStop(this, a),
            b || c("body").off(".treeview"),
            this._deactivate(),
            this.storedCursor && (this.document.find("body").css("cursor", this.storedCursor),
            this.storedStylesheet.remove()),
            c.ui.ddmanager && !b && (d = c.ui.ddmanager.drop(this, a)) ? (this.placeholder && (this.dragItems.parent().show(),
            this._removePlaceholder()),
            this.dragging = !1,
            this.dragItems = null,
            this.currentItem = null,
            this.helper.remove(),
            this.helper = null,
            void this._stop(a)) : a.target ? void (this.options.dragAnimate ? (e = this._getAnimation(),
            this.animating = !0,
            this.helper.animate(e, parseInt(this.options.dragAnimate, 10) || 500, function() {
                f._finishDrag(a)
            })) : this._finishDrag(a)) : (this.fromOutside = !1,
            void (this.dragging = !1))
        },
        _scrollCheck: function(a, b) {
            var d, e, f, g = 0, h = 0, i = this.options, j = this.scrollParent[0];
            return j && j !== document && "HTML" !== j.tagName ? (this.overflowOffset.top + j.offsetHeight - a.pageY < i.dragScrollSensitivity ? g = i.dragScrollSpeed : a.pageY - this.overflowOffset.top < i.dragScrollSensitivity && (g = -i.dragScrollSpeed),
            b && g && (d = j.scrollTop + g,
            d < 0 ? (j.scrollTop = 0,
            g = 0) : d > j.scrollHeight - j.clientHeight ? (j.scrollTop = j.scrollHeight - j.clientHeight,
            g = 0) : j.scrollTop = d),
            this.overflowOffset.left + j.offsetWidth - a.pageX < i.dragScrollSensitivity ? h = i.dragScrollSpeed : a.pageX - this.overflowOffset.left < i.dragScrollSensitivity && (h = -i.dragScrollSpeed),
            b && h && (e = j.scrollLeft + h,
            e < 0 ? (j.scrollLeft = 0,
            h = 0) : e > j.scrollWidth - j.clientWidth ? (j.scrollLeft = j.scrollWidth - j.clientWidth,
            h = 0) : j.scrollLeft = e),
            f = !(!h && !g)) : (d = c(document).scrollTop(),
            e = c(document).scrollLeft(),
            a.pageY - d < i.dragScrollSensitivity ? g = -i.dragScrollSpeed : c(window).height() - (a.pageY - d) < i.dragScrollSensitivity && (g = i.dragScrollSpeed),
            b && g && (d += g,
            d < 0 ? (c(document).scrollTop(0),
            g = 0) : d > c(document).height() - c(window).height() ? (c(document).scrollTop(c(document).height() - c(window).height()),
            g = 0) : (a.pageY += g,
            c(document).scrollTop(d))),
            a.pageX - e < i.dragScrollSensitivity ? h = -i.dragScrollSpeed : c(window).width() - (a.pageX - e) < i.dragScrollSensitivity && (h = i.dragScrollSpeed),
            b && h && (e += h,
            e < 0 ? (c(document).scrollLeft(0),
            h = 0) : e + this.helper.width() > c(document).width() - c(window).width() ? (c(document).scrollLeft(c(document).width() - c(window).width() - this.helper.width()),
            h = 0) : (a.pageX += h,
            c(document).scrollLeft(e))),
            f = !(!h && !g),
            f && b && (this.position = this._generatePosition(a),
            this.helper[0].style.left = this.position.left + "px",
            this.helper[0].style.top = this.position.top + "px",
            c.ui.ddmanager && c.ui.ddmanager.prepareOffsets(this, a))),
            f
        },
        _scrollStart: function(a) {
            function b() {
                c.scrollTimerId = setTimeout(function() {
                    c._scrollCheck(a, !0) ? (c._dragHitCheck(),
                    b()) : c._scrollStop()
                }, e[d]),
                d < e.length - 1 && (d += 1)
            }
            var c = this
              , d = 0
              , e = [150, 125, 100, 99, 96, 91, 84, 75, 64, 51, 36];
            this.scrollTimerId && this._scrollStop(),
            b()
        },
        _scrollStop: function() {
            clearTimeout(this.scrollTimerId),
            this.scrollTimerId = null
        },
        _getAnimation: function() {
            var a, b, c = {};
            return this.placeholder || this.dropTargetNode ? (this.placeholder ? (b = this.placeholder,
            a = b.offset()) : (b = this.dropTargetNode,
            a = b.offset()),
            c.left = a.left - this.offset.parent.left - this.margins.left,
            c.top = a.top - this.offset.parent.top - this.margins.top) : (b = this.dragItems.eq(0),
            a = this.originalPosition,
            c.left = a.left - this.margins.left,
            c.top = a.top - this.margins.top,
            this.scrollParent[0] !== document && (c.left += this.originalScroll.left - this.scrollParent[0].scrollLeft,
            c.top += this.originalScroll.top - this.scrollParent[0].scrollTop)),
            this.rtlFactor === -1 && (c.left += b.width() - this.helper.width()),
            c
        },
        _initPositions: function(a) {
            var b, e, f, h, i, j = this, k = [], l = this.options.dragReorder, m = this.nodeAdapter;
            if (this.dragItems && this.dragItems.length > 0 ? (i = this.getNodes(this.dragItems),
            i[0] || (i = [])) : i = [],
            a && this.dropPositions)
                for (e = [],
                h = a[0].id,
                f = 0; f < this.dropPositions.length && h !== this.dropPositions[f].nodeId; f++)
                    ;
            else
                e = this.dropPositions = [],
                a = this.element;
            if (a.find(t).each(function() {
                var a, b, d, f = !1, h = c(this);
                if (h.is(":visible") && !h.is("." + E)) {
                    if (l ? (b = h.parent().closest(t),
                    a = b.length ? j.treeMap[g(b)] : j.options.showRoot ? null : m.root()) : a = j.treeMap[g(h)],
                    !l && "move" === j.dragOperation && (i.indexOf(a) >= 0 || k.indexOf(h.parent().closest(t)[0]) >= 0))
                        return void k.push(this);
                    d = a && m.allowAdd(a, j.dragOperation, i),
                    l && (f = m.allowAdd(j.treeMap[g(h)], j.dragOperation, i)),
                    (d || f || h.hasClass(L)) && e.push({
                        canAdd: d,
                        canAddChild: f,
                        element: c(this).children(w),
                        nodeId: this.id,
                        top: 0,
                        bottom: 0
                    })
                }
            }),
            f !== d && e.length)
                for (b = 0; b < e.length; b++)
                    this.dropPositions.splice(f + b, 0, e[b])
        },
        _refreshPositions: function() {
            var a, b, c, d, e;
            for (a = 0; a < this.dropPositions.length; a++)
                b = this.dropPositions[a],
                d = b.element.outerHeight(),
                c = b.element.offset(),
                b.top = c.top,
                b.bottom = c.top + d;
            this.dropPositionsOrigin = 0,
            e = this.scrollParent,
            e && e[0] !== document ? this.dropPositionsOrigin = e[0].scrollTop : e = this.element,
            c = e.offset(),
            this.containerCache.left = c.left,
            this.containerCache.top = c.top,
            this.containerCache.width = e.outerWidth(),
            this.containerCache.height = e.outerHeight()
        },
        _makeTempDragItem: function() {
            var b, d, e, f = a.htmlBuilder();
            for (f.markup("<li").attr("class", r).markup("><div").attr("class", v).markup("></div><div").attr("class", x).markup(">unseen content</div></li>"),
            d = c(f.toString()),
            b = 0; b < this.dropPositions.length; b++)
                if (this.dropPositions[b].canAdd) {
                    e = c(this.dropPositions[b].nodeId).parent();
                    break
                }
            e || (e = this.element.children("ul")),
            e.append(d),
            this.dragItems = d.children(y)
        },
        _createPlaceholder: function(a) {
            this.placeholder = c("<li class='" + r + " " + E + "'><div class='" + v + "'></div><div class='" + x + "'>&nbsp;</div></li>"),
            this.dragItems.first().parent().before(this.placeholder),
            a && this.placeholder.height(a)
        },
        _movePlaceholder: function(a, b) {
            var d, e, f, h, i, j = this, k = this.placeholder.parent(), l = this.nodeAdapter, m = a.element.parent(), n = m[0];
            if ("after" === b && m.hasClass(M) && l.allowAdd(j.treeMap[g(m)], j.dragOperation) && (n = m.children("ul").children()[0],
            b = "before"),
            "above" === b) {
                if (m.next(":visible").length)
                    return;
                if (n = m.parent().parent()[0],
                m = c(n),
                e = m.parent().closest(t),
                i = e.length ? j.treeMap[g(e)] : j.options.showRoot ? null : l.root(),
                m.hasClass(q) || null === i)
                    return;
                if (f = l.allowAdd(i, j.dragOperation),
                !f)
                    return;
                b = "after"
            }
            if ("below" === b) {
                if (d = m.prevAll(":visible").first(),
                h = !1,
                d.hasClass(M) && (d = d.children("ul").children().last(),
                h = !0),
                0 === d.length)
                    return;
                if (f = l.allowAdd(j.treeMap[g(d)], j.dragOperation),
                !h && d.hasClass(O) && f && this._makeParentIfNeeded(d.children(y)),
                d.hasClass(L))
                    return void this._expandNode(d, function() {
                        j._initPositions(d),
                        j._refreshPositions(),
                        f && d.children("ul")[0].appendChild(j.placeholder[0])
                    });
                f && d[0].parentNode.appendChild(this.placeholder[0])
            } else
                "after" !== b || n.nextSibling ? n.parentNode.insertBefore(this.placeholder[0], "before" === b ? n : n.nextSibling) : n.parentNode.appendChild(this.placeholder[0]);
            0 === k.children().length && this._makeLeafIfNeeded(k.parent().find(y)),
            this._refreshPositions()
        },
        _removePlaceholder: function() {
            var a = this.placeholder.parent();
            this.placeholder.remove(),
            this.placeholder = null,
            0 === a.children().length && this._makeLeafIfNeeded(a.parent().find(y))
        },
        _createHelper: function(a) {
            var b, d = this.options;
            return c.isFunction(d.dragHelper) ? b = c(d.dragHelper.apply(this.element[0], [a, this.dragItems])) : 1 === this.dragItems.length ? b = this.dragItems.clone().removeAttr("id").removeClass(F) : (b = c("<div></div>"),
            b.html(this.dragItems.clone().removeClass(F))),
            b.parents("body").length || b.appendTo("parent" === d.dragAppendTo ? this.element[0].parentNode : d.dragAppendTo),
            /(fixed|absolute)/.test(b.css("position")) || b.css("position", "absolute"),
            b
        },
        _adjustOffsetFromHelper: function(a) {
            "left"in a && (this.offset.click.left = a.left + this.margins.left),
            "right"in a && (this.offset.click.left = this.helperProportions.width - a.right + this.margins.left),
            "top"in a && (this.offset.click.top = a.top + this.margins.top),
            "bottom"in a && (this.offset.click.top = this.helperProportions.height - a.bottom + this.margins.top)
        },
        _getParentOffset: function() {
            var a;
            return this.offsetParent = this.helper.offsetParent(),
            a = this.offsetParent.offset(),
            this.scrollParent && this.scrollParent[0] !== document && c.contains(this.scrollParent[0], this.offsetParent[0]) && (a.left += this.scrollParent.scrollLeft(),
            a.top += this.scrollParent.scrollTop()),
            (this.offsetParent[0] === document.body || this.offsetParent[0].tagName && "html" === this.offsetParent[0].tagName.toLowerCase() && c.ui.ie) && (a = {
                top: 0,
                left: 0
            }),
            {
                top: a.top + (parseInt(this.offsetParent.css("borderTopWidth"), 10) || 0),
                left: a.left + (parseInt(this.offsetParent.css("borderLeftWidth"), 10) || 0)
            }
        },
        _generatePosition: function(a) {
            var b = a.pageX
              , d = a.pageY
              , e = this.scrollParent && this.scrollParent[0] !== document && c.contains(this.scrollParent[0], this.offsetParent[0]) ? this.scrollParent : this.offsetParent
              , f = /(html|body)/i.test(e[0].tagName);
            return this.dragging || this.containment && (a.pageX - this.offset.click.left < this.containment[0] && (b = this.containment[0] + this.offset.click.left),
            a.pageY - this.offset.click.top < this.containment[1] && (d = this.containment[1] + this.offset.click.top),
            a.pageX - this.offset.click.left > this.containment[2] && (b = this.containment[2] + this.offset.click.left),
            a.pageY - this.offset.click.top > this.containment[3] && (d = this.containment[3] + this.offset.click.top)),
            {
                top: d - this.offset.click.top - this.offset.parent.top + (f ? 0 : e.scrollTop()),
                left: b - this.offset.click.left - this.offset.parent.left + (f ? 0 : e.scrollLeft())
            }
        },
        _adjustPositionForScroll: function() {
            var a = this.position
              , b = this.scrollParent && this.scrollParent[0] !== document && c.contains(this.scrollParent[0], this.offsetParent[0]) ? this.scrollParent : this.offsetParent
              , d = /(html|body)/i.test(b[0].tagName);
            return {
                top: a.top + this.offset.parent.top - (d ? 0 : b.scrollTop()),
                left: a.left + this.offset.parent.left - (d ? 0 : b.scrollLeft())
            }
        },
        _cacheHelperProportions: function() {
            this.helperProportions = {
                width: this.helper.outerWidth(),
                height: this.helper.outerHeight()
            }
        },
        _setContainment: function() {
            var a, b, d, e = this.options;
            "parent" === e.dragContainment && (e.dragContainment = this.helper[0].parentNode),
            "document" !== e.dragContainment && "window" !== e.dragContainment || (this.containment = [0 - this.offset.parent.left, 0 - this.offset.parent.top, c("document" === e.dragContainment ? document : window).width() - this.helperProportions.width - this.margins.left, (c("document" === e.dragContainment ? document : window).height() || document.body.parentNode.scrollHeight) - this.helperProportions.height - this.margins.top]),
            /^(document|window|parent)$/.test(e.dragContainment) || (a = c(e.dragContainment)[0],
            b = c(e.dragContainment).offset(),
            d = "hidden" !== c(a).css("overflow"),
            this.containment = [b.left + (parseInt(c(a).css("borderLeftWidth"), 10) || 0) + (parseInt(c(a).css("paddingLeft"), 10) || 0) - this.margins.left, b.top + (parseInt(c(a).css("borderTopWidth"), 10) || 0) + (parseInt(c(a).css("paddingTop"), 10) || 0) - this.margins.top, b.left + (d ? Math.max(a.scrollWidth, a.offsetWidth) : a.offsetWidth) - (parseInt(c(a).css("borderLeftWidth"), 10) || 0) - (parseInt(c(a).css("paddingRight"), 10) || 0) - this.helperProportions.width - this.margins.left, b.top + (d ? Math.max(a.scrollHeight, a.offsetHeight) : a.offsetHeight) - (parseInt(c(a).css("borderTopWidth"), 10) || 0) - (parseInt(c(a).css("paddingBottom"), 10) || 0) - this.helperProportions.height - this.margins.top])
        },
        _intersectsWith: function(a) {
            var b = this.positionAbs.left
              , c = this.positionAbs.top
              , d = a.left
              , e = d + a.width
              , f = a.top
              , g = f + a.height
              , h = this.offset.click.top
              , i = this.offset.click.left
              , j = c + h > f && c + h < g
              , k = b + i > d && b + i < e;
            return j && k
        },
        _dragCopyOrMove: function(a, b) {
            var c, d;
            a.ctrlKey ? c = "ctrl" : a.altKey ? c = "alt" : a.shiftKey ? c = "shift" : a.metaKey && (c = "meta"),
            d = this.dragOperations[c] || this.dragOperations.normal,
            this.dragOperation !== d && (this.dragOperation = d,
            this.placeholder && this.dragItems.parent().toggle("move" !== d),
            this._initPositions(),
            this._refreshPositions(),
            b && this._trigger("drag", a, this._uiHashDnD()))
        },
        _cancel: function(a, b) {
            function c() {
                e.animating = !1,
                e.helper && e.helper[0].parentNode && e.helper.remove(),
                e.helper = null,
                e.dragging = !1,
                e.dragItems = null,
                e.currentItem = null,
                e._stop(a)
            }
            var d, e = this;
            this.dragging && (this.positionAbs.top = -99999,
            this._mouseUp({
                target: null
            }),
            this.placeholder && this.dragItems.parent().show()),
            this.dropTargetNode = null,
            this.placeholder && this._removePlaceholder(),
            this.options.dragAnimate && !b ? (d = this._getAnimation(),
            this.animating = !0,
            this.helper.animate(d, parseInt(this.options.dragAnimate, 10) || 500, function() {
                c()
            })) : c()
        },
        _deactivate: function() {
            this.element.find("." + T).removeClass(T)
        },
        _finishDrag: function(a) {
            var c, d, e, h, i, j = !0, k = this.nodeAdapter;
            if (this.animating = !1,
            this.placeholder ? (d = this.placeholder.parent().closest(t),
            this.dragItems.parent().show(),
            e = f(this.placeholder),
            "move" === this.dragOperation && this.dragItems.parent().hide()) : (d = this.dropTargetNode,
            e = 0),
            this.fromOutside) {
                if (this.dragItems.parent().remove(),
                "add" === this.dragOperation && k.addNode)
                    try {
                        this.placeholder && this._removePlaceholder(),
                        this._add(a, d.children(y), e, null, !0)
                    } catch (l) {
                        b.error("Error in drop add action.", l)
                    }
            } else if (("copy" === this.dragOperation || "move" === this.dragOperation) && k.allowAdd && k["copy" === this.dragOperation ? "copyNodes" : "moveNodes"] && ("copy" === this.dragOperation || k.allowDelete))
                try {
                    if (h = d.length || this.options.showRoot ? this.treeMap[g(d)] : k.root(),
                    k.allowAdd(h, this.dragOperation, this.dragItems) && "move" === this.dragOperation)
                        for (i = this.getNodes(this.dragItems),
                        c = 0; c < i.length; c++)
                            if (!k.allowDelete(i[c])) {
                                j = !1;
                                break
                            }
                    if (j && "move" === this.dragOperation)
                        if (this.placeholder) {
                            if (this.dragItems.last().closest(t).next()[0] === this.placeholder[0]) {
                                for (j = !1,
                                c = 0; c < this.dragItems.length - 1; c++)
                                    if (this.dragItems.eq(c).closest(t).next()[0] !== this.dragItems.eq(c + 1).closest(t)[0]) {
                                        j = !0;
                                        break
                                    }
                            } else if (this.dragItems.first().closest(t).prev()[0] === this.placeholder[0])
                                for (j = !1,
                                c = 1; c < this.dragItems.length; c++)
                                    if (this.dragItems.eq(c).closest(t).prev()[0] !== this.dragItems.eq(c - 1).closest(t)[0]) {
                                        j = !0;
                                        break
                                    }
                        } else
                            for (j = !1,
                            c = 0; c < this.dragItems.length; c++)
                                if (this.dragItems.eq(c).closest(t).parent().closest(t)[0] !== d[0]) {
                                    j = !0;
                                    break
                                }
                    j ? (this.placeholder && this._removePlaceholder(),
                    this._moveOrCopy(a, d.children(y), e, this.dragItems, "copy" === this.dragOperation, !0)) : this.dragItems.parent().show()
                } catch (l) {
                    this.dragItems.parent().show(),
                    b.error("Error in drop " + this.dragOperation + " action.", l)
                }
            this.dragging = !1,
            this._trigger("beforeStop", a, this._uiHashDnD()),
            this.dragItems = null,
            this.currentItem = null,
            this.placeholder && this._removePlaceholder(),
            this.helper.remove(),
            this.helper = null,
            this.fromOutside && this._trigger("deactivate", a, this._uiHashDnD(this)),
            this._stop(a),
            this.fromOutside = !1
        },
        _stop: function(a) {
            apex.tooltipManager && apex.tooltipManager.enableTooltips(),
            this._trigger("stop", a, this._uiHashDnD())
        },
        _add: function(b, d, e, f, h) {
            var j, k, l = this, m = this.nodeAdapter;
            d && d.length ? (j = this.treeMap[g(d.parent())],
            k = i(d, this.labelSelector) + 1) : (d = null,
            j = m.root(),
            k = 1),
            m.addNode(j, e, null, f, function(f, g) {
                function i() {
                    l._select(q.node$, b, h),
                    l._trigger("added", b, q)
                }
                var m, n, o, p = a.htmlBuilder(), q = {
                    parentNode: j,
                    parent$: d,
                    node: f,
                    index: g
                };
                if (!(f === !1 || null === f || g < 0)) {
                    if (d) {
                        if (l._makeParentIfNeeded(d),
                        n = d.parent().children("ul"),
                        0 === n.length)
                            return void l._expandNode(d.parent(), function() {
                                n = d.parent().children("ul"),
                                q.node$ = n.children().eq(e).children(y),
                                i()
                            })
                    } else
                        n = l.element.children("ul");
                    l._renderNode(f, k, p),
                    m = c(p.toString()),
                    q.node$ = m.children(y),
                    o = n.children(),
                    g >= o.length ? n.append(m) : o.eq(g).before(m),
                    i()
                }
            })
        },
        _moveOrCopy: function(b, d, e, f, h, j) {
            var k, l, m = this, n = this.getNodes(f), o = h ? "copyNodes" : "moveNodes", p = this.nodeAdapter;
            d && d.length ? (k = this.treeMap[g(d.parent())],
            l = i(d, this.labelSelector) + 1) : (d = null,
            k = p.root(),
            l = 1),
            p[o](k, e, n, function(e) {
                function g() {
                    for (i = 0; i < x.length; i++)
                        s = x[i],
                        o = p.child(k, s.toIndex),
                        s.toNode = o,
                        w.clear(),
                        m._renderNode(o, l, w),
                        q = c(w.toString()),
                        s.toNode$ = q.children(y),
                        v = u.children(":visible"),
                        s.toIndex >= v.length ? u.append(q) : v.eq(s.toIndex).before(q),
                        z.push(s.toNode$[0]),
                        h || (r = s.fromNode$.parent().parent().closest(t).children(y),
                        s.fromParent$ = r,
                        s.fromIndex = s.fromNode$.parent().parent().children().index(s.fromNode$.parent()),
                        s.fromNode$.parent().remove(),
                        m._makeLeafIfNeeded(r));
                    m._select(c(z), b, j),
                    m._trigger(h ? "copied" : "moved", b, A)
                }
                var i, n, o, q, r, s, u, v, w = a.htmlBuilder(), x = [], z = [], A = {
                    parentNode: k,
                    parent$: d,
                    items: x
                };
                if (e) {
                    for (i = 0; i < e.length; i++)
                        n = e[i],
                        n >= 0 && x.push({
                            fromNode$: f.eq(i),
                            toIndex: n
                        });
                    if (x.sort(function(a, b) {
                        return a.toIndex - b.toIndex
                    }),
                    d)
                        return m._makeParentIfNeeded(d),
                        u = d.parent().children("ul"),
                        void m._expandNode(d.parent(), function() {
                            g()
                        });
                    u = m.element.children("ul"),
                    g()
                }
            })
        },
        _uiHashDnD: function(a) {
            var b = a || this;
            return {
                helper: b.helper,
                placeholder: b.dropTargetNode || b.placeholder || c([]),
                position: b.position,
                originalPosition: b.originalPosition,
                offset: b.positionAbs,
                items: b.dragItems,
                operation: b.dragOperation,
                sender: a ? a.element : null
            }
        }
    });
    var _ = {
        root: function() {
            return this.data
        },
        getLabel: function(a) {
            return a.label
        },
        getIcon: function(a) {
            var b = this.getType(a)
              , c = null;
            return a.icon || null === a.icon ? c = a.icon : b.icon || null === b.icon ? c = b.icon : this.types["default"].icon !== d && (c = this.types["default"].icon),
            c
        },
        getClasses: function(a) {
            var b = this.getType(a)
              , c = null;
            return b.classes ? c = b.classes : this.types["default"].classes && (c = this.types["default"].classes),
            a.classes && (c ? c += " " + a.classes : c = a.classes),
            c
        },
        getLink: function(a) {
            return a.link
        },
        isDisabled: function(a) {
            var b = this.getType(a)
              , c = !1;
            return a.isDisabled !== d ? c = a.isDisabled : b.isDisabled !== d ? c = b.isDisabled : this.types["default"].isDisabled !== d && (c = this.types["default"].isDisabled),
            c
        },
        child: function(a, b) {
            if (a.children)
                return a.children[b]
        },
        childCount: function(a) {
            return a.children ? a.children.length : 0
        },
        hasChildren: function(a) {
            return !!a.children && a.children.length > 0
        },
        allowAdd: function(a, b, c) {
            var e, f, g = this.getType(a), h = !!a.children && this.check("canAdd", a, b, c);
            if (h && c && (g.validChildren !== d ? f = g.validChildren : this.types["default"].validChildren !== d && (f = this.types["default"].validChildren),
            f !== !0))
                for (e = 0; e < c.length; e++)
                    if (f.indexOf(c[e].type) < 0) {
                        h = !1;
                        break
                    }
            return h
        },
        allowRename: function(a) {
            return this.check("canRename", a)
        },
        allowDelete: function(a) {
            return a !== this.data && this.check("canDelete", a)
        },
        allowDrag: function(a) {
            return this.check("canDrag", a)
        },
        dragOperations: function(a) {
            var b, c, e;
            if (a) {
                if (a.length > 0) {
                    for (e = a[0].type || "default",
                    b = 1; b < a.length; b++)
                        if (a[b].type !== e) {
                            e = "default";
                            break
                        }
                } else
                    e = "default";
                c = this.types[e].operations && this.types[e].operations.drag !== d ? this.types[e].operations.drag : this.types["default"].operations.drag
            } else
                c = this.types["default"].operations.externalDrag;
            return c
        },
        addNode: function(a, b, e, f, g) {
            var h, i = c.extend(!0, {}, f || this.newNode(a));
            e && (i.label = e),
            this.sortCompare ? a.children.push(i) : a.children.splice(b, 0, i),
            i._parent = a,
            this._nextId !== d && (i.id === d ? i.id = this.nextId() : this._nextId += 1),
            this.sortCompare && a.children.sort(this.sortCompare),
            h = a.children.indexOf(i),
            this.validateAdd(i, h, function(b) {
                "string" == typeof b || b === !1 ? (a.children.splice(h, 1),
                g(b === !1 && null)) : b && g(i, h)
            })
        },
        renameNode: function(a, b, c) {
            var d, e = a.label;
            a.label = b,
            a._parent ? (this.sortCompare && a._parent.children.sort(this.sortCompare),
            d = a._parent.children.indexOf(a)) : d = 0,
            this.validateRename(a, d, function(b) {
                "string" == typeof b || b === !1 ? (a.label = e,
                c(b === !1 && null)) : b && c(a, d)
            })
        },
        deleteNode: function(a, b, c) {
            var d = a._parent
              , e = a._parent.children.indexOf(a);
            d.children.splice(e, 1),
            delete a._parent,
            this.validateDelete(a, c, function(c) {
                c || (a._parent = d,
                d.children.splice(e, 0, a)),
                b(c)
            })
        },
        moveNodes: function(a, b, c, d) {
            var e, f, g, h, i = [];
            for (e = 0; e < c.length; e++)
                f = c[e],
                g = f._parent,
                h = g.children.indexOf(f),
                g.children.splice(h, 1),
                a === g && h < b && (b -= 1),
                this.sortCompare ? a.children.push(f) : (a.children.splice(b, 0, f),
                b += 1),
                f._parent = a;
            for (this.sortCompare && a.children.sort(this.sortCompare),
            e = 0; e < c.length; e++)
                i[e] = a.children.indexOf(c[e]);
            this.validateMove(a, c, i, function(a) {
                d(!!a && i)
            })
        },
        copyNodes: function(a, b, e, f) {
            function g(a, b) {
                var e, f = c.extend({}, a);
                if (f._parent = b,
                k._nextId !== d && (f.id = k.nextId()),
                a.children)
                    for (f.children = [],
                    e = 0; e < a.children.length; e++)
                        f.children.push(g(a.children[e], f));
                return f
            }
            var h, i, j, k = this, l = [], m = [];
            for (h = 0; h < e.length; h++)
                i = e[h],
                j = g(i, a),
                l[h] = j,
                this.sortCompare ? a.children.push(j) : (a.children.splice(b, 0, j),
                m[h] = b,
                b += 1);
            if (this.sortCompare)
                for (a.children.sort(this.sortCompare),
                h = 0; h < l.length; h++)
                    m[h] = a.children.indexOf(l[h]);
            this.validateCopy(a, l, m, function(a) {
                f(!!a && m)
            })
        },
        sortCompare: function(a, b) {
            return a.label > b.label ? 1 : a.label < b.label ? -1 : 0
        },
        nextId: function() {
            var a = this._nextId;
            return this._nextId += 1,
            "tn" + a
        },
        newNode: function(a) {
            var b, e = {}, f = !0, g = this.getType(a);
            return this._nextId !== d && (e.id = this.nextId()),
            c.isArray(g.validChildren) ? (e.type = g.validChildren[0],
            b = this.types[e.type],
            b && b.operations && b.operations.canAdd !== d ? f = g.operations.canAdd : this.types["default"].operations.canAdd !== d && (f = this.types["default"].operations.canAdd),
            b && b.defaultLabel !== d ? e.label = b.defaultLabel : this.types["default"].defaultLabel !== d && (e.label = this.types["default"].defaultLabel)) : this.types["default"].defaultLabel !== d && (e.label = this.types["default"].defaultLabel),
            f && (e.children = []),
            e
        },
        extraCheck: function(a, b, c, d, e) {
            return a
        },
        validateAdd: function(a, b, c) {
            c(!0)
        },
        validateRename: function(a, b, c) {
            c(!0)
        },
        validateDelete: function(a, b, c) {
            c(!0)
        },
        validateMove: function(a, b, c, d) {
            d(!0)
        },
        validateCopy: function(a, b, c, d) {
            d(!0)
        },
        getType: function(a) {
            var b = "default";
            return a.type && (b = a.type),
            this.types[b] || this.types["default"]
        },
        check: function(a, b, e, f) {
            var g = !1
              , h = this.getType(b);
            return b.operations && b.operations[a] !== d ? g = b.operations[a] : h.operations && h.operations[a] !== d ? g = h.operations[a] : this.types["default"].operations[a] !== d && (g = this.types["default"].operations[a]),
            c.isFunction(g) && (g = g.call(this, b, e, f)),
            this.extraCheck(g, a, b, e, f)
        }
    };
    if (c.apex.treeView.makeDefaultNodeAdapter = function(a, b, e, f) {
        function g(a, b) {
            var c;
            if (a._parent = b,
            e && (h._nextId += 1),
            a.children)
                for (c = 0; c < a.children.length; c++)
                    g(a.children[c], a)
        }
        var h = Object.create(_);
        return c.isArray(e) && (f = e,
        e = !0),
        null !== e && e !== d || (e = !0),
        e && (this.addViewStateMixin(h, "id", f),
        h._nextId = 1),
        h.data = a,
        h.types = c.extend(!0, {}, {
            "default": {
                isDisabled: !1,
                validChildren: !0,
                operations: {
                    canAdd: !0,
                    canRename: !0,
                    canDelete: !0,
                    canDrag: !0,
                    drag: {
                        normal: "move",
                        ctrl: "copy"
                    },
                    externalDrag: {
                        normal: "add"
                    }
                }
            }
        }, b),
        h.data && g(h.data, null),
        h
    }
    ,
    c.apex.treeView.makeModelNodeAdapter = function(a, b, c) {
        var e, f;
        if (!apex.model)
            throw "Missing module apex.model";
        return b.shape = "tree",
        e = apex.model.create(a, b, c),
        f = b.labelField || "label",
        e._labelKey = e.getFieldKey(f),
        e._iconKey = e.getFieldKey(b.iconField || "icon"),
        e._classesKey = e.getFieldKey(b.classesField || "classes"),
        e._linkKey = e.getFieldKey(b.linkField || "link"),
        e._disabledKey = e.getFieldKey(b.disabledField || "isDisabled"),
        b.hasIdentity && this.addViewStateMixin(e, function(a) {
            return e.getRecordId(a)
        }, b.initialExpandedNodeIds),
        e.getType = e._getType,
        e.getLabel = function(a) {
            return a[this._labelKey]
        }
        ,
        e.getIcon = function(a) {
            var b = this.getType(a)
              , c = this._options
              , e = null;
            return this._iconKey && (a[this._iconKey] || null === a[this._iconKey]) ? e = a[this._iconKey] : b.icon || null === b.icon ? e = b.icon : c.types["default"].icon !== d && (e = c.types["default"].icon),
            e
        }
        ,
        e.getClasses = function(a) {
            var b = this.getType(a)
              , c = this._options
              , d = null;
            return b.classes ? d = b.classes : c.types["default"].classes && (d = c.types["default"].classes),
            this._classesKey && a[this._classesKey] && (d ? d += " " + a[this._classesKey] : d = a[this._classesKey]),
            d
        }
        ,
        e.getLink = function(a) {
            return this._linkKey ? a[this._linkKey] : null
        }
        ,
        e.isDisabled = function(a) {
            var b = this.getType(a)
              , c = this._options
              , e = !1;
            return this._disabledKey && a[this._disabledKey] !== d ? e = a[this._disabledKey] : b.isDisabled !== d ? e = b.isDisabled : c.types["default"].isDisabled !== d && (e = c.types["default"].isDisabled),
            e
        }
        ,
        e.allowRename = e.allowEdit,
        e.addNode = function(a, b, c, d, e) {
            var f, g, h, i = null, j = this._initRecord(d, null, a);
            g = a[this._childrenKey],
            b >= 0 && b < g.length && (i = g[b]),
            c && (j[this._labelKey] = c),
            h = this.insertNewRecord(a, i, j),
            j = this.getRecord(h),
            f = g.indexOf(j),
            e(j, f)
        }
        ,
        e.renameNode = function(a, b, c) {
            var d, e;
            this.setValue(a, f, b),
            e = this.parent(a),
            d = e ? e[this._childrenKey].indexOf(a) : 0,
            c(a, d)
        }
        ,
        e.deleteNode = function(a, b, c) {
            var d = this.deleteRecords([a]);
            b(1 === d)
        }
        ,
        e.moveNodes = function(a, b, c, d) {
            var e, f, g, h = null, i = [], j = [];
            for (g = a[this._childrenKey],
            b -= 1,
            b >= 0 && b < g.length && (h = g[b]),
            i = this.moveRecords(c, a, h),
            e = 0; e < i.length; e++)
                f = this.getRecord(i[e]),
                j[e] = g.indexOf(f);
            d(j)
        }
        ,
        e.copyNodes = function(a, b, c, d) {
            var e, f, g, h = null, i = [], j = [];
            for (g = a[this._childrenKey],
            b -= 1,
            b >= 0 && b < g.length && (h = g[b]),
            i = this.copyRecords(c, a, h),
            e = 0; e < i.length; e++)
                f = this.getRecord(i[e]),
                j[e] = g.indexOf(f);
            d(j)
        }
        ,
        e
    }
    ,
    c.apex.treeView.treeModelListener = function(a, b) {
        function d(a, b) {
            function d(a) {
                var b, d, e = [];
                for (b = 0; b < a.length; b++)
                    d = h.getViewId(g.baseId, a[b]),
                    e.push(c("#" + g.baseId + d).children(y)[0]);
                return c(e)
            }
            var e, f;
            if ("refresh" === a)
                g.refresh();
            else if ("refreshRecords" === a || "revert" === a)
                ;
            else if ("move" === a)
                ;
            else if ("copy" === a)
                ;
            else if ("insert" === a)
                f = d([h.parent(b.record)]),
                g.refresh(f);
            else if ("clearChanges" === a)
                ;
            else if ("delete" === a) {
                for (f = d(b.records),
                e = 0; e < b.records.length; e++)
                    h.clearViewId(g.baseId, b.records[e]);
                g.deleteTreeNodes(f)
            } else
                "set" !== a && "metaChange" !== a || (f = d([b.record]),
                g.update(f))
        }
        var e, f, g = b.data("apex-treeView"), h = g.getNodeAdapter();
        if (f = g.option("treeModel"),
        f && (f.unSubscribe(g.option("modelViewId")),
        g.option("modelName") !== a && apex.model.release(this.modelName),
        g.option("treeModel", null),
        g.option("modelName", null),
        g.option("modelViewId", null)),
        a) {
            if (g.option("treeModel", a),
            f = apex.model.get(a),
            g.option("modelName", f),
            !f)
                throw new Error("TreeView model not found: " + a);
            g.option("modelViewId", f.subscribe({
                onChange: d,
                progressView: this.element
            })),
            e = f.getOption("onlyMarkForDelete")
        }
    }
    ,
    c.apex.treeView.addViewStateMixin = function(a, b, d) {
        c.extend(a, {
            _state: {},
            isExpanded: function(a, b) {
                var c = this._getExpandedNodes(a);
                return c[this._getIdentity(b)] || !1
            },
            setExpanded: function(a, b, c) {
                var d = this._getExpandedNodes(a);
                d[this._getIdentity(b)] = c
            },
            getExpandedNodeIds: function(a) {
                var b, c = [], d = this._getExpandedNodes(a);
                for (b in d)
                    d.hasOwnProperty(b) && d[b] === !0 && c.push(b);
                return c
            },
            getExpandedState: function(a) {
                var b = this._getExpandedNodes(a);
                return c.extend({}, b)
            },
            getViewId: function(a, b) {
                var c = this._state[a] && this._state[a].nodeMap;
                return c && c[this._getIdentity(b)]
            },
            setViewId: function(a, b, c) {
                var d = this._state[a] && this._state[a].nodeMap;
                d || (d = {},
                this._state[a] || (this._state[a] = {}),
                this._state[a].nodeMap = d),
                d[this._getIdentity(b)] = c
            },
            clearViewId: function(a, b) {
                var c = this._state[a] && this._state[a].nodeMap
                  , d = this._state[a] && this._state[a].expandedNodes;
                c && (b ? (delete c[this._getIdentity(b)],
                d && delete d[this._getIdentity(b)]) : (this._state[a].nodeMap = {},
                delete this._state[a].expandedNodes))
            },
            _getExpandedNodes: function(a) {
                var b, c = this._state[a] && this._state[a].expandedNodes;
                if (!c && (this._state[a] || (this._state[a] = {}),
                c = {},
                this._state[a].expandedNodes = c,
                d))
                    for (b = 0; b < d.length; b++)
                        c[d[b]] = !0;
                return c
            }
        }),
        a._getIdentity || (a._getIdentity = c.isFunction(b) ? b : function(a) {
            return a[b]
        }
        )
    }
    ,
    c.ui.draggable && (c.ui.plugin.add("draggable", "connectToTreeView", {
        start: function(a, d) {
            var e = c(this).data("ui-draggable")
              , f = e.options
              , g = c.extend({}, d, {
                item: e.element
            });
            c("body").on("keydown.treeviewplug", function(a) {
                a.keyCode === c.ui.keyCode.ESCAPE && (e.dropped = !1,
                e.cancel())
            }),
            e.trees = [],
            c(f.connectToTreeView).each(function() {
                var d = c.data(this, "apex-treeView");
                d && !d.options.disabled && d.options.dragAndDrop ? (e.trees.push({
                    instance: d
                }),
                d._initPositions(),
                d._refreshPositions(),
                d._trigger("activate", a, g)) : b.warn("Draggable connectToTreeView matches an element that is not a treeView, is disabled, or doesn't support drag and drop.")
            })
        },
        stop: function(a, b) {
            var d = c(this).data("ui-draggable");
            c("body").off(".treeviewplug"),
            c.each(d.trees, function() {
                this.instance.isOver && !this.invalid ? (this.instance.isOver = !1,
                d.cancelHelperRemoval = !0,
                this.instance._mouseStop(a, !0),
                a.target || (this.instance._trigger("deactivate", a, this.instance._uiHashDnD(this.instance)),
                this.instance.dragItems.parent().remove(),
                this.instance._cancel(a, !0))) : (this.instance._deactivate(),
                this.instance._trigger("deactivate", a, this.instance._uiHashDnD(this.instance)),
                this.instance.dragItems && (this.instance.dragItems.parent().remove(),
                this.instance._cancel(a, !0)))
            })
        },
        drag: function(a, b) {
            var d = c(this).data("ui-draggable");
            c.each(d.trees, function() {
                var c = !1;
                if (!this.invalid)
                    if (this.instance.positionAbs = d.positionAbs,
                    this.instance.helperProportions = d.helperProportions,
                    this.instance.offset.click = d.offset.click,
                    this.instance._intersectsWith(this.instance.containerCache) && (c = !0),
                    c) {
                        if (!this.instance.isOver) {
                            if (this.instance.isOver = !0,
                            this.instance._makeTempDragItem(),
                            this.instance.helper = b.helper,
                            this.instance.helper.css("position", "relative"),
                            a.target = this.instance.dragItems.parent().children(w)[0],
                            !this.instance._mouseCapture(a, !0))
                                return this.instance.isOver = !1,
                                void (this.invalid = !0);
                            this.instance._trigger("over", a, this.instance._uiHashDnD(this.instance)),
                            this.instance._mouseStart(a, a, !0),
                            this.instance.offset.click.top = d.offset.click.top,
                            this.instance.offset.click.left = d.offset.click.left,
                            this.instance.offset.parent.left -= d.offset.parent.left - this.instance.offset.parent.left,
                            this.instance.offset.parent.top -= d.offset.parent.top - this.instance.offset.parent.top,
                            d.dropped = this.instance.element,
                            d.currentItem = d.element,
                            this.instance.fromOutside = d
                        }
                        this.instance.dragItems && this.instance._mouseDrag(a)
                    } else
                        this.instance.isOver && (this.instance.isOver = !1,
                        this.instance._trigger("out", a, this.instance._uiHashDnD(this.instance)),
                        a.target = null,
                        this.instance._mouseStop(a, !0),
                        this.instance.dragItems.parent().remove(),
                        this.instance.placeholder && this.instance._removePlaceholder(),
                        d.dropped = !1)
            })
        }
    }),
    c.ui.plugin.add("draggable", "cursor2", {
        start: function() {
            var a = c("body")
              , b = c(this).data("ui-draggable")
              , d = b.options;
            d.cursor2 && "auto" !== d.cursor2 && (b.storedCursor = a.css("cursor"),
            a.css("cursor", d.cursor2),
            b.storedStylesheet = c("<style>*{ cursor: " + d.cursor2 + " !important; }</style>").appendTo(a))
        },
        stop: function() {
            var a = c(this).data("ui-draggable");
            a.storedCursor && (c("body").css("cursor", a.storedCursor),
            a.storedStylesheet.remove())
        }
    })),
    apex.widget)
        if (apex.widget.tree)
            b.warn("Old and new tree implementations cannot be mixed.");
        else {
            var aa = {
                "default": {
                    icon: "icon-tree-folder",
                    operations: {
                        canAdd: !1,
                        canDelete: !1,
                        canRename: !1,
                        canDrag: !1
                    }
                }
            };
            apex.widget.tree = {
                init: function(b, d, e, f, g, h, i, j, k) {
                    var l, m = c.extend(!0, {}, aa, d), n = c("#" + a.escapeCSS(b), apex.gPageContext$);
                    n.treeView({
                        getNodeAdapter: function() {
                            return c.apex.treeView.makeDefaultNodeAdapter(e, m, h)
                        },
                        navigation: !0,
                        doubleClick: "D" === f && "activate",
                        tooltip: j ? {
                            show: apex.tooltipManager.defaultShowOption(),
                            content: function(a, b) {
                                return b ? b.tooltip : null
                            }
                        } : null,
                        multiple: !1,
                        showRoot: !i,
                        expandRoot: !0,
                        iconType: k
                    }),
                    g && (l = n.treeView("find", {
                        depth: -1,
                        findAll: !1,
                        match: function(a) {
                            return a.id === g
                        }
                    }),
                    l.length && n.treeView("setSelection", l))
                },
                expand_all: function(b) {
                    c("#" + a.escapeCSS(b), apex.gPageContext$).treeView("expandAll")
                },
                collapse_all: function(b) {
                    c("#" + a.escapeCSS(b), apex.gPageContext$).treeView("collapseAll")
                },
                reset: function(b) {
                    var d = c("#" + a.escapeCSS(b), apex.gPageContext$);
                    d.treeView("collapseAll").treeView("expand", d.children().children("li").first())
                }
            }
        }
}(apex.util, apex.debug, apex.jQuery);

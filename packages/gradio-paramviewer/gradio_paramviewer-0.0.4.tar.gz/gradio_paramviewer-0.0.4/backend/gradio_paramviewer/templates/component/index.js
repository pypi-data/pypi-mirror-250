var xe = typeof globalThis < "u" ? globalThis : typeof window < "u" ? window : typeof global < "u" ? global : typeof self < "u" ? self : {};
function Ft(l) {
  return l && l.__esModule && Object.prototype.hasOwnProperty.call(l, "default") ? l.default : l;
}
var ut = { exports: {} };
(function(l) {
  var t = typeof window < "u" ? window : typeof WorkerGlobalScope < "u" && self instanceof WorkerGlobalScope ? self : {};
  /**
   * Prism: Lightweight, robust, elegant syntax highlighting
   *
   * @license MIT <https://opensource.org/licenses/MIT>
   * @author Lea Verou <https://lea.verou.me>
   * @namespace
   * @public
   */
  var e = function(n) {
    var s = /(?:^|\s)lang(?:uage)?-([\w-]+)(?=\s|$)/i, a = 0, r = {}, i = {
      /**
       * By default, Prism will attempt to highlight all code elements (by calling {@link Prism.highlightAll}) on the
       * current page after the page finished loading. This might be a problem if e.g. you wanted to asynchronously load
       * additional languages or plugins yourself.
       *
       * By setting this value to `true`, Prism will not automatically highlight all code elements on the page.
       *
       * You obviously have to change this value before the automatic highlighting started. To do this, you can add an
       * empty Prism object into the global scope before loading the Prism script like this:
       *
       * ```js
       * window.Prism = window.Prism || {};
       * Prism.manual = true;
       * // add a new <script> to load Prism's script
       * ```
       *
       * @default false
       * @type {boolean}
       * @memberof Prism
       * @public
       */
      manual: n.Prism && n.Prism.manual,
      /**
       * By default, if Prism is in a web worker, it assumes that it is in a worker it created itself, so it uses
       * `addEventListener` to communicate with its parent instance. However, if you're using Prism manually in your
       * own worker, you don't want it to do this.
       *
       * By setting this value to `true`, Prism will not add its own listeners to the worker.
       *
       * You obviously have to change this value before Prism executes. To do this, you can add an
       * empty Prism object into the global scope before loading the Prism script like this:
       *
       * ```js
       * window.Prism = window.Prism || {};
       * Prism.disableWorkerMessageHandler = true;
       * // Load Prism's script
       * ```
       *
       * @default false
       * @type {boolean}
       * @memberof Prism
       * @public
       */
      disableWorkerMessageHandler: n.Prism && n.Prism.disableWorkerMessageHandler,
      /**
       * A namespace for utility methods.
       *
       * All function in this namespace that are not explicitly marked as _public_ are for __internal use only__ and may
       * change or disappear at any time.
       *
       * @namespace
       * @memberof Prism
       */
      util: {
        encode: function c(o) {
          return o instanceof u ? new u(o.type, c(o.content), o.alias) : Array.isArray(o) ? o.map(c) : o.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/\u00a0/g, " ");
        },
        /**
         * Returns the name of the type of the given value.
         *
         * @param {any} o
         * @returns {string}
         * @example
         * type(null)      === 'Null'
         * type(undefined) === 'Undefined'
         * type(123)       === 'Number'
         * type('foo')     === 'String'
         * type(true)      === 'Boolean'
         * type([1, 2])    === 'Array'
         * type({})        === 'Object'
         * type(String)    === 'Function'
         * type(/abc+/)    === 'RegExp'
         */
        type: function(c) {
          return Object.prototype.toString.call(c).slice(8, -1);
        },
        /**
         * Returns a unique number for the given object. Later calls will still return the same number.
         *
         * @param {Object} obj
         * @returns {number}
         */
        objId: function(c) {
          return c.__id || Object.defineProperty(c, "__id", { value: ++a }), c.__id;
        },
        /**
         * Creates a deep clone of the given object.
         *
         * The main intended use of this function is to clone language definitions.
         *
         * @param {T} o
         * @param {Record<number, any>} [visited]
         * @returns {T}
         * @template T
         */
        clone: function c(o, d) {
          d = d || {};
          var g, p;
          switch (i.util.type(o)) {
            case "Object":
              if (p = i.util.objId(o), d[p])
                return d[p];
              g = /** @type {Record<string, any>} */
              {}, d[p] = g;
              for (var b in o)
                o.hasOwnProperty(b) && (g[b] = c(o[b], d));
              return (
                /** @type {any} */
                g
              );
            case "Array":
              return p = i.util.objId(o), d[p] ? d[p] : (g = [], d[p] = g, /** @type {Array} */
              /** @type {any} */
              o.forEach(function(E, v) {
                g[v] = c(E, d);
              }), /** @type {any} */
              g);
            default:
              return o;
          }
        },
        /**
         * Returns the Prism language of the given element set by a `language-xxxx` or `lang-xxxx` class.
         *
         * If no language is set for the element or the element is `null` or `undefined`, `none` will be returned.
         *
         * @param {Element} element
         * @returns {string}
         */
        getLanguage: function(c) {
          for (; c; ) {
            var o = s.exec(c.className);
            if (o)
              return o[1].toLowerCase();
            c = c.parentElement;
          }
          return "none";
        },
        /**
         * Sets the Prism `language-xxxx` class of the given element.
         *
         * @param {Element} element
         * @param {string} language
         * @returns {void}
         */
        setLanguage: function(c, o) {
          c.className = c.className.replace(RegExp(s, "gi"), ""), c.classList.add("language-" + o);
        },
        /**
         * Returns the script element that is currently executing.
         *
         * This does __not__ work for line script element.
         *
         * @returns {HTMLScriptElement | null}
         */
        currentScript: function() {
          if (typeof document > "u")
            return null;
          if ("currentScript" in document && 1 < 2)
            return (
              /** @type {any} */
              document.currentScript
            );
          try {
            throw new Error();
          } catch (g) {
            var c = (/at [^(\r\n]*\((.*):[^:]+:[^:]+\)$/i.exec(g.stack) || [])[1];
            if (c) {
              var o = document.getElementsByTagName("script");
              for (var d in o)
                if (o[d].src == c)
                  return o[d];
            }
            return null;
          }
        },
        /**
         * Returns whether a given class is active for `element`.
         *
         * The class can be activated if `element` or one of its ancestors has the given class and it can be deactivated
         * if `element` or one of its ancestors has the negated version of the given class. The _negated version_ of the
         * given class is just the given class with a `no-` prefix.
         *
         * Whether the class is active is determined by the closest ancestor of `element` (where `element` itself is
         * closest ancestor) that has the given class or the negated version of it. If neither `element` nor any of its
         * ancestors have the given class or the negated version of it, then the default activation will be returned.
         *
         * In the paradoxical situation where the closest ancestor contains __both__ the given class and the negated
         * version of it, the class is considered active.
         *
         * @param {Element} element
         * @param {string} className
         * @param {boolean} [defaultActivation=false]
         * @returns {boolean}
         */
        isActive: function(c, o, d) {
          for (var g = "no-" + o; c; ) {
            var p = c.classList;
            if (p.contains(o))
              return !0;
            if (p.contains(g))
              return !1;
            c = c.parentElement;
          }
          return !!d;
        }
      },
      /**
       * This namespace contains all currently loaded languages and the some helper functions to create and modify languages.
       *
       * @namespace
       * @memberof Prism
       * @public
       */
      languages: {
        /**
         * The grammar for plain, unformatted text.
         */
        plain: r,
        plaintext: r,
        text: r,
        txt: r,
        /**
         * Creates a deep copy of the language with the given id and appends the given tokens.
         *
         * If a token in `redef` also appears in the copied language, then the existing token in the copied language
         * will be overwritten at its original position.
         *
         * ## Best practices
         *
         * Since the position of overwriting tokens (token in `redef` that overwrite tokens in the copied language)
         * doesn't matter, they can technically be in any order. However, this can be confusing to others that trying to
         * understand the language definition because, normally, the order of tokens matters in Prism grammars.
         *
         * Therefore, it is encouraged to order overwriting tokens according to the positions of the overwritten tokens.
         * Furthermore, all non-overwriting tokens should be placed after the overwriting ones.
         *
         * @param {string} id The id of the language to extend. This has to be a key in `Prism.languages`.
         * @param {Grammar} redef The new tokens to append.
         * @returns {Grammar} The new language created.
         * @public
         * @example
         * Prism.languages['css-with-colors'] = Prism.languages.extend('css', {
         *     // Prism.languages.css already has a 'comment' token, so this token will overwrite CSS' 'comment' token
         *     // at its original position
         *     'comment': { ... },
         *     // CSS doesn't have a 'color' token, so this token will be appended
         *     'color': /\b(?:red|green|blue)\b/
         * });
         */
        extend: function(c, o) {
          var d = i.util.clone(i.languages[c]);
          for (var g in o)
            d[g] = o[g];
          return d;
        },
        /**
         * Inserts tokens _before_ another token in a language definition or any other grammar.
         *
         * ## Usage
         *
         * This helper method makes it easy to modify existing languages. For example, the CSS language definition
         * not only defines CSS highlighting for CSS documents, but also needs to define highlighting for CSS embedded
         * in HTML through `<style>` elements. To do this, it needs to modify `Prism.languages.markup` and add the
         * appropriate tokens. However, `Prism.languages.markup` is a regular JavaScript object literal, so if you do
         * this:
         *
         * ```js
         * Prism.languages.markup.style = {
         *     // token
         * };
         * ```
         *
         * then the `style` token will be added (and processed) at the end. `insertBefore` allows you to insert tokens
         * before existing tokens. For the CSS example above, you would use it like this:
         *
         * ```js
         * Prism.languages.insertBefore('markup', 'cdata', {
         *     'style': {
         *         // token
         *     }
         * });
         * ```
         *
         * ## Special cases
         *
         * If the grammars of `inside` and `insert` have tokens with the same name, the tokens in `inside`'s grammar
         * will be ignored.
         *
         * This behavior can be used to insert tokens after `before`:
         *
         * ```js
         * Prism.languages.insertBefore('markup', 'comment', {
         *     'comment': Prism.languages.markup.comment,
         *     // tokens after 'comment'
         * });
         * ```
         *
         * ## Limitations
         *
         * The main problem `insertBefore` has to solve is iteration order. Since ES2015, the iteration order for object
         * properties is guaranteed to be the insertion order (except for integer keys) but some browsers behave
         * differently when keys are deleted and re-inserted. So `insertBefore` can't be implemented by temporarily
         * deleting properties which is necessary to insert at arbitrary positions.
         *
         * To solve this problem, `insertBefore` doesn't actually insert the given tokens into the target object.
         * Instead, it will create a new object and replace all references to the target object with the new one. This
         * can be done without temporarily deleting properties, so the iteration order is well-defined.
         *
         * However, only references that can be reached from `Prism.languages` or `insert` will be replaced. I.e. if
         * you hold the target object in a variable, then the value of the variable will not change.
         *
         * ```js
         * var oldMarkup = Prism.languages.markup;
         * var newMarkup = Prism.languages.insertBefore('markup', 'comment', { ... });
         *
         * assert(oldMarkup !== Prism.languages.markup);
         * assert(newMarkup === Prism.languages.markup);
         * ```
         *
         * @param {string} inside The property of `root` (e.g. a language id in `Prism.languages`) that contains the
         * object to be modified.
         * @param {string} before The key to insert before.
         * @param {Grammar} insert An object containing the key-value pairs to be inserted.
         * @param {Object<string, any>} [root] The object containing `inside`, i.e. the object that contains the
         * object to be modified.
         *
         * Defaults to `Prism.languages`.
         * @returns {Grammar} The new grammar object.
         * @public
         */
        insertBefore: function(c, o, d, g) {
          g = g || /** @type {any} */
          i.languages;
          var p = g[c], b = {};
          for (var E in p)
            if (p.hasOwnProperty(E)) {
              if (E == o)
                for (var v in d)
                  d.hasOwnProperty(v) && (b[v] = d[v]);
              d.hasOwnProperty(E) || (b[E] = p[E]);
            }
          var T = g[c];
          return g[c] = b, i.languages.DFS(i.languages, function(z, O) {
            O === T && z != c && (this[z] = b);
          }), b;
        },
        // Traverse a language definition with Depth First Search
        DFS: function c(o, d, g, p) {
          p = p || {};
          var b = i.util.objId;
          for (var E in o)
            if (o.hasOwnProperty(E)) {
              d.call(o, E, o[E], g || E);
              var v = o[E], T = i.util.type(v);
              T === "Object" && !p[b(v)] ? (p[b(v)] = !0, c(v, d, null, p)) : T === "Array" && !p[b(v)] && (p[b(v)] = !0, c(v, d, E, p));
            }
        }
      },
      plugins: {},
      /**
       * This is the most high-level function in Prism’s API.
       * It fetches all the elements that have a `.language-xxxx` class and then calls {@link Prism.highlightElement} on
       * each one of them.
       *
       * This is equivalent to `Prism.highlightAllUnder(document, async, callback)`.
       *
       * @param {boolean} [async=false] Same as in {@link Prism.highlightAllUnder}.
       * @param {HighlightCallback} [callback] Same as in {@link Prism.highlightAllUnder}.
       * @memberof Prism
       * @public
       */
      highlightAll: function(c, o) {
        i.highlightAllUnder(document, c, o);
      },
      /**
       * Fetches all the descendants of `container` that have a `.language-xxxx` class and then calls
       * {@link Prism.highlightElement} on each one of them.
       *
       * The following hooks will be run:
       * 1. `before-highlightall`
       * 2. `before-all-elements-highlight`
       * 3. All hooks of {@link Prism.highlightElement} for each element.
       *
       * @param {ParentNode} container The root element, whose descendants that have a `.language-xxxx` class will be highlighted.
       * @param {boolean} [async=false] Whether each element is to be highlighted asynchronously using Web Workers.
       * @param {HighlightCallback} [callback] An optional callback to be invoked on each element after its highlighting is done.
       * @memberof Prism
       * @public
       */
      highlightAllUnder: function(c, o, d) {
        var g = {
          callback: d,
          container: c,
          selector: 'code[class*="language-"], [class*="language-"] code, code[class*="lang-"], [class*="lang-"] code'
        };
        i.hooks.run("before-highlightall", g), g.elements = Array.prototype.slice.apply(g.container.querySelectorAll(g.selector)), i.hooks.run("before-all-elements-highlight", g);
        for (var p = 0, b; b = g.elements[p++]; )
          i.highlightElement(b, o === !0, g.callback);
      },
      /**
       * Highlights the code inside a single element.
       *
       * The following hooks will be run:
       * 1. `before-sanity-check`
       * 2. `before-highlight`
       * 3. All hooks of {@link Prism.highlight}. These hooks will be run by an asynchronous worker if `async` is `true`.
       * 4. `before-insert`
       * 5. `after-highlight`
       * 6. `complete`
       *
       * Some the above hooks will be skipped if the element doesn't contain any text or there is no grammar loaded for
       * the element's language.
       *
       * @param {Element} element The element containing the code.
       * It must have a class of `language-xxxx` to be processed, where `xxxx` is a valid language identifier.
       * @param {boolean} [async=false] Whether the element is to be highlighted asynchronously using Web Workers
       * to improve performance and avoid blocking the UI when highlighting very large chunks of code. This option is
       * [disabled by default](https://prismjs.com/faq.html#why-is-asynchronous-highlighting-disabled-by-default).
       *
       * Note: All language definitions required to highlight the code must be included in the main `prism.js` file for
       * asynchronous highlighting to work. You can build your own bundle on the
       * [Download page](https://prismjs.com/download.html).
       * @param {HighlightCallback} [callback] An optional callback to be invoked after the highlighting is done.
       * Mostly useful when `async` is `true`, since in that case, the highlighting is done asynchronously.
       * @memberof Prism
       * @public
       */
      highlightElement: function(c, o, d) {
        var g = i.util.getLanguage(c), p = i.languages[g];
        i.util.setLanguage(c, g);
        var b = c.parentElement;
        b && b.nodeName.toLowerCase() === "pre" && i.util.setLanguage(b, g);
        var E = c.textContent, v = {
          element: c,
          language: g,
          grammar: p,
          code: E
        };
        function T(O) {
          v.highlightedCode = O, i.hooks.run("before-insert", v), v.element.innerHTML = v.highlightedCode, i.hooks.run("after-highlight", v), i.hooks.run("complete", v), d && d.call(v.element);
        }
        if (i.hooks.run("before-sanity-check", v), b = v.element.parentElement, b && b.nodeName.toLowerCase() === "pre" && !b.hasAttribute("tabindex") && b.setAttribute("tabindex", "0"), !v.code) {
          i.hooks.run("complete", v), d && d.call(v.element);
          return;
        }
        if (i.hooks.run("before-highlight", v), !v.grammar) {
          T(i.util.encode(v.code));
          return;
        }
        if (o && n.Worker) {
          var z = new Worker(i.filename);
          z.onmessage = function(O) {
            T(O.data);
          }, z.postMessage(JSON.stringify({
            language: v.language,
            code: v.code,
            immediateClose: !0
          }));
        } else
          T(i.highlight(v.code, v.grammar, v.language));
      },
      /**
       * Low-level function, only use if you know what you’re doing. It accepts a string of text as input
       * and the language definitions to use, and returns a string with the HTML produced.
       *
       * The following hooks will be run:
       * 1. `before-tokenize`
       * 2. `after-tokenize`
       * 3. `wrap`: On each {@link Token}.
       *
       * @param {string} text A string with the code to be highlighted.
       * @param {Grammar} grammar An object containing the tokens to use.
       *
       * Usually a language definition like `Prism.languages.markup`.
       * @param {string} language The name of the language definition passed to `grammar`.
       * @returns {string} The highlighted HTML.
       * @memberof Prism
       * @public
       * @example
       * Prism.highlight('var foo = true;', Prism.languages.javascript, 'javascript');
       */
      highlight: function(c, o, d) {
        var g = {
          code: c,
          grammar: o,
          language: d
        };
        if (i.hooks.run("before-tokenize", g), !g.grammar)
          throw new Error('The language "' + g.language + '" has no grammar.');
        return g.tokens = i.tokenize(g.code, g.grammar), i.hooks.run("after-tokenize", g), u.stringify(i.util.encode(g.tokens), g.language);
      },
      /**
       * This is the heart of Prism, and the most low-level function you can use. It accepts a string of text as input
       * and the language definitions to use, and returns an array with the tokenized code.
       *
       * When the language definition includes nested tokens, the function is called recursively on each of these tokens.
       *
       * This method could be useful in other contexts as well, as a very crude parser.
       *
       * @param {string} text A string with the code to be highlighted.
       * @param {Grammar} grammar An object containing the tokens to use.
       *
       * Usually a language definition like `Prism.languages.markup`.
       * @returns {TokenStream} An array of strings and tokens, a token stream.
       * @memberof Prism
       * @public
       * @example
       * let code = `var foo = 0;`;
       * let tokens = Prism.tokenize(code, Prism.languages.javascript);
       * tokens.forEach(token => {
       *     if (token instanceof Prism.Token && token.type === 'number') {
       *         console.log(`Found numeric literal: ${token.content}`);
       *     }
       * });
       */
      tokenize: function(c, o) {
        var d = o.rest;
        if (d) {
          for (var g in d)
            o[g] = d[g];
          delete o.rest;
        }
        var p = new y();
        return F(p, p.head, c), _(c, p, o, p.head, 0), k(p);
      },
      /**
       * @namespace
       * @memberof Prism
       * @public
       */
      hooks: {
        all: {},
        /**
         * Adds the given callback to the list of callbacks for the given hook.
         *
         * The callback will be invoked when the hook it is registered for is run.
         * Hooks are usually directly run by a highlight function but you can also run hooks yourself.
         *
         * One callback function can be registered to multiple hooks and the same hook multiple times.
         *
         * @param {string} name The name of the hook.
         * @param {HookCallback} callback The callback function which is given environment variables.
         * @public
         */
        add: function(c, o) {
          var d = i.hooks.all;
          d[c] = d[c] || [], d[c].push(o);
        },
        /**
         * Runs a hook invoking all registered callbacks with the given environment variables.
         *
         * Callbacks will be invoked synchronously and in the order in which they were registered.
         *
         * @param {string} name The name of the hook.
         * @param {Object<string, any>} env The environment variables of the hook passed to all callbacks registered.
         * @public
         */
        run: function(c, o) {
          var d = i.hooks.all[c];
          if (!(!d || !d.length))
            for (var g = 0, p; p = d[g++]; )
              p(o);
        }
      },
      Token: u
    };
    n.Prism = i;
    function u(c, o, d, g) {
      this.type = c, this.content = o, this.alias = d, this.length = (g || "").length | 0;
    }
    u.stringify = function c(o, d) {
      if (typeof o == "string")
        return o;
      if (Array.isArray(o)) {
        var g = "";
        return o.forEach(function(T) {
          g += c(T, d);
        }), g;
      }
      var p = {
        type: o.type,
        content: c(o.content, d),
        tag: "span",
        classes: ["token", o.type],
        attributes: {},
        language: d
      }, b = o.alias;
      b && (Array.isArray(b) ? Array.prototype.push.apply(p.classes, b) : p.classes.push(b)), i.hooks.run("wrap", p);
      var E = "";
      for (var v in p.attributes)
        E += " " + v + '="' + (p.attributes[v] || "").replace(/"/g, "&quot;") + '"';
      return "<" + p.tag + ' class="' + p.classes.join(" ") + '"' + E + ">" + p.content + "</" + p.tag + ">";
    };
    function f(c, o, d, g) {
      c.lastIndex = o;
      var p = c.exec(d);
      if (p && g && p[1]) {
        var b = p[1].length;
        p.index += b, p[0] = p[0].slice(b);
      }
      return p;
    }
    function _(c, o, d, g, p, b) {
      for (var E in d)
        if (!(!d.hasOwnProperty(E) || !d[E])) {
          var v = d[E];
          v = Array.isArray(v) ? v : [v];
          for (var T = 0; T < v.length; ++T) {
            if (b && b.cause == E + "," + T)
              return;
            var z = v[T], O = z.inside, G = !!z.lookbehind, J = !!z.greedy, H = z.alias;
            if (J && !z.pattern.global) {
              var de = z.pattern.toString().match(/[imsuy]*$/)[0];
              z.pattern = RegExp(z.pattern.source, de + "g");
            }
            for (var ge = z.pattern || z, M = g.next, j = p; M !== o.tail && !(b && j >= b.reach); j += M.value.length, M = M.next) {
              var X = M.value;
              if (o.length > c.length)
                return;
              if (!(X instanceof u)) {
                var ne = 1, D;
                if (J) {
                  if (D = f(ge, j, c, G), !D || D.index >= c.length)
                    break;
                  var _e = D.index, w = D.index + D[0].length, K = j;
                  for (K += M.value.length; _e >= K; )
                    M = M.next, K += M.value.length;
                  if (K -= M.value.length, j = K, M.value instanceof u)
                    continue;
                  for (var ue = M; ue !== o.tail && (K < w || typeof ue.value == "string"); ue = ue.next)
                    ne++, K += ue.value.length;
                  ne--, X = c.slice(j, K), D.index -= j;
                } else if (D = f(ge, 0, X, G), !D)
                  continue;
                var _e = D.index, pe = D[0], Ae = X.slice(0, _e), Te = X.slice(_e + pe.length), Se = j + X.length;
                b && Se > b.reach && (b.reach = Se);
                var me = M.prev;
                Ae && (me = F(o, me, Ae), j += Ae.length), m(o, me, ne);
                var kt = new u(E, O ? i.tokenize(pe, O) : pe, H, pe);
                if (M = F(o, me, kt), Te && F(o, M, Te), ne > 1) {
                  var Ee = {
                    cause: E + "," + T,
                    reach: Se
                  };
                  _(c, o, d, M.prev, j, Ee), b && Ee.reach > b.reach && (b.reach = Ee.reach);
                }
              }
            }
          }
        }
    }
    function y() {
      var c = { value: null, prev: null, next: null }, o = { value: null, prev: c, next: null };
      c.next = o, this.head = c, this.tail = o, this.length = 0;
    }
    function F(c, o, d) {
      var g = o.next, p = { value: d, prev: o, next: g };
      return o.next = p, g.prev = p, c.length++, p;
    }
    function m(c, o, d) {
      for (var g = o.next, p = 0; p < d && g !== c.tail; p++)
        g = g.next;
      o.next = g, g.prev = o, c.length -= p;
    }
    function k(c) {
      for (var o = [], d = c.head.next; d !== c.tail; )
        o.push(d.value), d = d.next;
      return o;
    }
    if (!n.document)
      return n.addEventListener && (i.disableWorkerMessageHandler || n.addEventListener("message", function(c) {
        var o = JSON.parse(c.data), d = o.language, g = o.code, p = o.immediateClose;
        n.postMessage(i.highlight(g, i.languages[d], d)), p && n.close();
      }, !1)), i;
    var q = i.util.currentScript();
    q && (i.filename = q.src, q.hasAttribute("data-manual") && (i.manual = !0));
    function h() {
      i.manual || i.highlightAll();
    }
    if (!i.manual) {
      var C = document.readyState;
      C === "loading" || C === "interactive" && q && q.defer ? document.addEventListener("DOMContentLoaded", h) : window.requestAnimationFrame ? window.requestAnimationFrame(h) : window.setTimeout(h, 16);
    }
    return i;
  }(t);
  l.exports && (l.exports = e), typeof xe < "u" && (xe.Prism = e), e.languages.markup = {
    comment: {
      pattern: /<!--(?:(?!<!--)[\s\S])*?-->/,
      greedy: !0
    },
    prolog: {
      pattern: /<\?[\s\S]+?\?>/,
      greedy: !0
    },
    doctype: {
      // https://www.w3.org/TR/xml/#NT-doctypedecl
      pattern: /<!DOCTYPE(?:[^>"'[\]]|"[^"]*"|'[^']*')+(?:\[(?:[^<"'\]]|"[^"]*"|'[^']*'|<(?!!--)|<!--(?:[^-]|-(?!->))*-->)*\]\s*)?>/i,
      greedy: !0,
      inside: {
        "internal-subset": {
          pattern: /(^[^\[]*\[)[\s\S]+(?=\]>$)/,
          lookbehind: !0,
          greedy: !0,
          inside: null
          // see below
        },
        string: {
          pattern: /"[^"]*"|'[^']*'/,
          greedy: !0
        },
        punctuation: /^<!|>$|[[\]]/,
        "doctype-tag": /^DOCTYPE/i,
        name: /[^\s<>'"]+/
      }
    },
    cdata: {
      pattern: /<!\[CDATA\[[\s\S]*?\]\]>/i,
      greedy: !0
    },
    tag: {
      pattern: /<\/?(?!\d)[^\s>\/=$<%]+(?:\s(?:\s*[^\s>\/=]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s'">=]+(?=[\s>]))|(?=[\s/>])))+)?\s*\/?>/,
      greedy: !0,
      inside: {
        tag: {
          pattern: /^<\/?[^\s>\/]+/,
          inside: {
            punctuation: /^<\/?/,
            namespace: /^[^\s>\/:]+:/
          }
        },
        "special-attr": [],
        "attr-value": {
          pattern: /=\s*(?:"[^"]*"|'[^']*'|[^\s'">=]+)/,
          inside: {
            punctuation: [
              {
                pattern: /^=/,
                alias: "attr-equals"
              },
              {
                pattern: /^(\s*)["']|["']$/,
                lookbehind: !0
              }
            ]
          }
        },
        punctuation: /\/?>/,
        "attr-name": {
          pattern: /[^\s>\/]+/,
          inside: {
            namespace: /^[^\s>\/:]+:/
          }
        }
      }
    },
    entity: [
      {
        pattern: /&[\da-z]{1,8};/i,
        alias: "named-entity"
      },
      /&#x?[\da-f]{1,8};/i
    ]
  }, e.languages.markup.tag.inside["attr-value"].inside.entity = e.languages.markup.entity, e.languages.markup.doctype.inside["internal-subset"].inside = e.languages.markup, e.hooks.add("wrap", function(n) {
    n.type === "entity" && (n.attributes.title = n.content.replace(/&amp;/, "&"));
  }), Object.defineProperty(e.languages.markup.tag, "addInlined", {
    /**
     * Adds an inlined language to markup.
     *
     * An example of an inlined language is CSS with `<style>` tags.
     *
     * @param {string} tagName The name of the tag that contains the inlined language. This name will be treated as
     * case insensitive.
     * @param {string} lang The language key.
     * @example
     * addInlined('style', 'css');
     */
    value: function(s, a) {
      var r = {};
      r["language-" + a] = {
        pattern: /(^<!\[CDATA\[)[\s\S]+?(?=\]\]>$)/i,
        lookbehind: !0,
        inside: e.languages[a]
      }, r.cdata = /^<!\[CDATA\[|\]\]>$/i;
      var i = {
        "included-cdata": {
          pattern: /<!\[CDATA\[[\s\S]*?\]\]>/i,
          inside: r
        }
      };
      i["language-" + a] = {
        pattern: /[\s\S]+/,
        inside: e.languages[a]
      };
      var u = {};
      u[s] = {
        pattern: RegExp(/(<__[^>]*>)(?:<!\[CDATA\[(?:[^\]]|\](?!\]>))*\]\]>|(?!<!\[CDATA\[)[\s\S])*?(?=<\/__>)/.source.replace(/__/g, function() {
          return s;
        }), "i"),
        lookbehind: !0,
        greedy: !0,
        inside: i
      }, e.languages.insertBefore("markup", "cdata", u);
    }
  }), Object.defineProperty(e.languages.markup.tag, "addAttribute", {
    /**
     * Adds an pattern to highlight languages embedded in HTML attributes.
     *
     * An example of an inlined language is CSS with `style` attributes.
     *
     * @param {string} attrName The name of the tag that contains the inlined language. This name will be treated as
     * case insensitive.
     * @param {string} lang The language key.
     * @example
     * addAttribute('style', 'css');
     */
    value: function(n, s) {
      e.languages.markup.tag.inside["special-attr"].push({
        pattern: RegExp(
          /(^|["'\s])/.source + "(?:" + n + ")" + /\s*=\s*(?:"[^"]*"|'[^']*'|[^\s'">=]+(?=[\s>]))/.source,
          "i"
        ),
        lookbehind: !0,
        inside: {
          "attr-name": /^[^\s=]+/,
          "attr-value": {
            pattern: /=[\s\S]+/,
            inside: {
              value: {
                pattern: /(^=\s*(["']|(?!["'])))\S[\s\S]*(?=\2$)/,
                lookbehind: !0,
                alias: [s, "language-" + s],
                inside: e.languages[s]
              },
              punctuation: [
                {
                  pattern: /^=/,
                  alias: "attr-equals"
                },
                /"|'/
              ]
            }
          }
        }
      });
    }
  }), e.languages.html = e.languages.markup, e.languages.mathml = e.languages.markup, e.languages.svg = e.languages.markup, e.languages.xml = e.languages.extend("markup", {}), e.languages.ssml = e.languages.xml, e.languages.atom = e.languages.xml, e.languages.rss = e.languages.xml, function(n) {
    var s = /(?:"(?:\\(?:\r\n|[\s\S])|[^"\\\r\n])*"|'(?:\\(?:\r\n|[\s\S])|[^'\\\r\n])*')/;
    n.languages.css = {
      comment: /\/\*[\s\S]*?\*\//,
      atrule: {
        pattern: RegExp("@[\\w-](?:" + /[^;{\s"']|\s+(?!\s)/.source + "|" + s.source + ")*?" + /(?:;|(?=\s*\{))/.source),
        inside: {
          rule: /^@[\w-]+/,
          "selector-function-argument": {
            pattern: /(\bselector\s*\(\s*(?![\s)]))(?:[^()\s]|\s+(?![\s)])|\((?:[^()]|\([^()]*\))*\))+(?=\s*\))/,
            lookbehind: !0,
            alias: "selector"
          },
          keyword: {
            pattern: /(^|[^\w-])(?:and|not|only|or)(?![\w-])/,
            lookbehind: !0
          }
          // See rest below
        }
      },
      url: {
        // https://drafts.csswg.org/css-values-3/#urls
        pattern: RegExp("\\burl\\((?:" + s.source + "|" + /(?:[^\\\r\n()"']|\\[\s\S])*/.source + ")\\)", "i"),
        greedy: !0,
        inside: {
          function: /^url/i,
          punctuation: /^\(|\)$/,
          string: {
            pattern: RegExp("^" + s.source + "$"),
            alias: "url"
          }
        }
      },
      selector: {
        pattern: RegExp(`(^|[{}\\s])[^{}\\s](?:[^{};"'\\s]|\\s+(?![\\s{])|` + s.source + ")*(?=\\s*\\{)"),
        lookbehind: !0
      },
      string: {
        pattern: s,
        greedy: !0
      },
      property: {
        pattern: /(^|[^-\w\xA0-\uFFFF])(?!\s)[-_a-z\xA0-\uFFFF](?:(?!\s)[-\w\xA0-\uFFFF])*(?=\s*:)/i,
        lookbehind: !0
      },
      important: /!important\b/i,
      function: {
        pattern: /(^|[^-a-z0-9])[-a-z0-9]+(?=\()/i,
        lookbehind: !0
      },
      punctuation: /[(){};:,]/
    }, n.languages.css.atrule.inside.rest = n.languages.css;
    var a = n.languages.markup;
    a && (a.tag.addInlined("style", "css"), a.tag.addAttribute("style", "css"));
  }(e), e.languages.clike = {
    comment: [
      {
        pattern: /(^|[^\\])\/\*[\s\S]*?(?:\*\/|$)/,
        lookbehind: !0,
        greedy: !0
      },
      {
        pattern: /(^|[^\\:])\/\/.*/,
        lookbehind: !0,
        greedy: !0
      }
    ],
    string: {
      pattern: /(["'])(?:\\(?:\r\n|[\s\S])|(?!\1)[^\\\r\n])*\1/,
      greedy: !0
    },
    "class-name": {
      pattern: /(\b(?:class|extends|implements|instanceof|interface|new|trait)\s+|\bcatch\s+\()[\w.\\]+/i,
      lookbehind: !0,
      inside: {
        punctuation: /[.\\]/
      }
    },
    keyword: /\b(?:break|catch|continue|do|else|finally|for|function|if|in|instanceof|new|null|return|throw|try|while)\b/,
    boolean: /\b(?:false|true)\b/,
    function: /\b\w+(?=\()/,
    number: /\b0x[\da-f]+\b|(?:\b\d+(?:\.\d*)?|\B\.\d+)(?:e[+-]?\d+)?/i,
    operator: /[<>]=?|[!=]=?=?|--?|\+\+?|&&?|\|\|?|[?*/~^%]/,
    punctuation: /[{}[\];(),.:]/
  }, e.languages.javascript = e.languages.extend("clike", {
    "class-name": [
      e.languages.clike["class-name"],
      {
        pattern: /(^|[^$\w\xA0-\uFFFF])(?!\s)[_$A-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*(?=\.(?:constructor|prototype))/,
        lookbehind: !0
      }
    ],
    keyword: [
      {
        pattern: /((?:^|\})\s*)catch\b/,
        lookbehind: !0
      },
      {
        pattern: /(^|[^.]|\.\.\.\s*)\b(?:as|assert(?=\s*\{)|async(?=\s*(?:function\b|\(|[$\w\xA0-\uFFFF]|$))|await|break|case|class|const|continue|debugger|default|delete|do|else|enum|export|extends|finally(?=\s*(?:\{|$))|for|from(?=\s*(?:['"]|$))|function|(?:get|set)(?=\s*(?:[#\[$\w\xA0-\uFFFF]|$))|if|implements|import|in|instanceof|interface|let|new|null|of|package|private|protected|public|return|static|super|switch|this|throw|try|typeof|undefined|var|void|while|with|yield)\b/,
        lookbehind: !0
      }
    ],
    // Allow for all non-ASCII characters (See http://stackoverflow.com/a/2008444)
    function: /#?(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*(?=\s*(?:\.\s*(?:apply|bind|call)\s*)?\()/,
    number: {
      pattern: RegExp(
        /(^|[^\w$])/.source + "(?:" + // constant
        (/NaN|Infinity/.source + "|" + // binary integer
        /0[bB][01]+(?:_[01]+)*n?/.source + "|" + // octal integer
        /0[oO][0-7]+(?:_[0-7]+)*n?/.source + "|" + // hexadecimal integer
        /0[xX][\dA-Fa-f]+(?:_[\dA-Fa-f]+)*n?/.source + "|" + // decimal bigint
        /\d+(?:_\d+)*n/.source + "|" + // decimal number (integer or float) but no bigint
        /(?:\d+(?:_\d+)*(?:\.(?:\d+(?:_\d+)*)?)?|\.\d+(?:_\d+)*)(?:[Ee][+-]?\d+(?:_\d+)*)?/.source) + ")" + /(?![\w$])/.source
      ),
      lookbehind: !0
    },
    operator: /--|\+\+|\*\*=?|=>|&&=?|\|\|=?|[!=]==|<<=?|>>>?=?|[-+*/%&|^!=<>]=?|\.{3}|\?\?=?|\?\.?|[~:]/
  }), e.languages.javascript["class-name"][0].pattern = /(\b(?:class|extends|implements|instanceof|interface|new)\s+)[\w.\\]+/, e.languages.insertBefore("javascript", "keyword", {
    regex: {
      pattern: RegExp(
        // lookbehind
        // eslint-disable-next-line regexp/no-dupe-characters-character-class
        /((?:^|[^$\w\xA0-\uFFFF."'\])\s]|\b(?:return|yield))\s*)/.source + // Regex pattern:
        // There are 2 regex patterns here. The RegExp set notation proposal added support for nested character
        // classes if the `v` flag is present. Unfortunately, nested CCs are both context-free and incompatible
        // with the only syntax, so we have to define 2 different regex patterns.
        /\//.source + "(?:" + /(?:\[(?:[^\]\\\r\n]|\\.)*\]|\\.|[^/\\\[\r\n])+\/[dgimyus]{0,7}/.source + "|" + // `v` flag syntax. This supports 3 levels of nested character classes.
        /(?:\[(?:[^[\]\\\r\n]|\\.|\[(?:[^[\]\\\r\n]|\\.|\[(?:[^[\]\\\r\n]|\\.)*\])*\])*\]|\\.|[^/\\\[\r\n])+\/[dgimyus]{0,7}v[dgimyus]{0,7}/.source + ")" + // lookahead
        /(?=(?:\s|\/\*(?:[^*]|\*(?!\/))*\*\/)*(?:$|[\r\n,.;:})\]]|\/\/))/.source
      ),
      lookbehind: !0,
      greedy: !0,
      inside: {
        "regex-source": {
          pattern: /^(\/)[\s\S]+(?=\/[a-z]*$)/,
          lookbehind: !0,
          alias: "language-regex",
          inside: e.languages.regex
        },
        "regex-delimiter": /^\/|\/$/,
        "regex-flags": /^[a-z]+$/
      }
    },
    // This must be declared before keyword because we use "function" inside the look-forward
    "function-variable": {
      pattern: /#?(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*(?=\s*[=:]\s*(?:async\s*)?(?:\bfunction\b|(?:\((?:[^()]|\([^()]*\))*\)|(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*)\s*=>))/,
      alias: "function"
    },
    parameter: [
      {
        pattern: /(function(?:\s+(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*)?\s*\(\s*)(?!\s)(?:[^()\s]|\s+(?![\s)])|\([^()]*\))+(?=\s*\))/,
        lookbehind: !0,
        inside: e.languages.javascript
      },
      {
        pattern: /(^|[^$\w\xA0-\uFFFF])(?!\s)[_$a-z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*(?=\s*=>)/i,
        lookbehind: !0,
        inside: e.languages.javascript
      },
      {
        pattern: /(\(\s*)(?!\s)(?:[^()\s]|\s+(?![\s)])|\([^()]*\))+(?=\s*\)\s*=>)/,
        lookbehind: !0,
        inside: e.languages.javascript
      },
      {
        pattern: /((?:\b|\s|^)(?!(?:as|async|await|break|case|catch|class|const|continue|debugger|default|delete|do|else|enum|export|extends|finally|for|from|function|get|if|implements|import|in|instanceof|interface|let|new|null|of|package|private|protected|public|return|set|static|super|switch|this|throw|try|typeof|undefined|var|void|while|with|yield)(?![$\w\xA0-\uFFFF]))(?:(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*\s*)\(\s*|\]\s*\(\s*)(?!\s)(?:[^()\s]|\s+(?![\s)])|\([^()]*\))+(?=\s*\)\s*\{)/,
        lookbehind: !0,
        inside: e.languages.javascript
      }
    ],
    constant: /\b[A-Z](?:[A-Z_]|\dx?)*\b/
  }), e.languages.insertBefore("javascript", "string", {
    hashbang: {
      pattern: /^#!.*/,
      greedy: !0,
      alias: "comment"
    },
    "template-string": {
      pattern: /`(?:\\[\s\S]|\$\{(?:[^{}]|\{(?:[^{}]|\{[^}]*\})*\})+\}|(?!\$\{)[^\\`])*`/,
      greedy: !0,
      inside: {
        "template-punctuation": {
          pattern: /^`|`$/,
          alias: "string"
        },
        interpolation: {
          pattern: /((?:^|[^\\])(?:\\{2})*)\$\{(?:[^{}]|\{(?:[^{}]|\{[^}]*\})*\})+\}/,
          lookbehind: !0,
          inside: {
            "interpolation-punctuation": {
              pattern: /^\$\{|\}$/,
              alias: "punctuation"
            },
            rest: e.languages.javascript
          }
        },
        string: /[\s\S]+/
      }
    },
    "string-property": {
      pattern: /((?:^|[,{])[ \t]*)(["'])(?:\\(?:\r\n|[\s\S])|(?!\2)[^\\\r\n])*\2(?=\s*:)/m,
      lookbehind: !0,
      greedy: !0,
      alias: "property"
    }
  }), e.languages.insertBefore("javascript", "operator", {
    "literal-property": {
      pattern: /((?:^|[,{])[ \t]*)(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*(?=\s*:)/m,
      lookbehind: !0,
      alias: "property"
    }
  }), e.languages.markup && (e.languages.markup.tag.addInlined("script", "javascript"), e.languages.markup.tag.addAttribute(
    /on(?:abort|blur|change|click|composition(?:end|start|update)|dblclick|error|focus(?:in|out)?|key(?:down|up)|load|mouse(?:down|enter|leave|move|out|over|up)|reset|resize|scroll|select|slotchange|submit|unload|wheel)/.source,
    "javascript"
  )), e.languages.js = e.languages.javascript, function() {
    if (typeof e > "u" || typeof document > "u")
      return;
    Element.prototype.matches || (Element.prototype.matches = Element.prototype.msMatchesSelector || Element.prototype.webkitMatchesSelector);
    var n = "Loading…", s = function(q, h) {
      return "✖ Error " + q + " while fetching file: " + h;
    }, a = "✖ Error: File does not exist or is empty", r = {
      js: "javascript",
      py: "python",
      rb: "ruby",
      ps1: "powershell",
      psm1: "powershell",
      sh: "bash",
      bat: "batch",
      h: "c",
      tex: "latex"
    }, i = "data-src-status", u = "loading", f = "loaded", _ = "failed", y = "pre[data-src]:not([" + i + '="' + f + '"]):not([' + i + '="' + u + '"])';
    function F(q, h, C) {
      var c = new XMLHttpRequest();
      c.open("GET", q, !0), c.onreadystatechange = function() {
        c.readyState == 4 && (c.status < 400 && c.responseText ? h(c.responseText) : c.status >= 400 ? C(s(c.status, c.statusText)) : C(a));
      }, c.send(null);
    }
    function m(q) {
      var h = /^\s*(\d+)\s*(?:(,)\s*(?:(\d+)\s*)?)?$/.exec(q || "");
      if (h) {
        var C = Number(h[1]), c = h[2], o = h[3];
        return c ? o ? [C, Number(o)] : [C, void 0] : [C, C];
      }
    }
    e.hooks.add("before-highlightall", function(q) {
      q.selector += ", " + y;
    }), e.hooks.add("before-sanity-check", function(q) {
      var h = (
        /** @type {HTMLPreElement} */
        q.element
      );
      if (h.matches(y)) {
        q.code = "", h.setAttribute(i, u);
        var C = h.appendChild(document.createElement("CODE"));
        C.textContent = n;
        var c = h.getAttribute("data-src"), o = q.language;
        if (o === "none") {
          var d = (/\.(\w+)$/.exec(c) || [, "none"])[1];
          o = r[d] || d;
        }
        e.util.setLanguage(C, o), e.util.setLanguage(h, o);
        var g = e.plugins.autoloader;
        g && g.loadLanguages(o), F(
          c,
          function(p) {
            h.setAttribute(i, f);
            var b = m(h.getAttribute("data-range"));
            if (b) {
              var E = p.split(/\r\n?|\n/g), v = b[0], T = b[1] == null ? E.length : b[1];
              v < 0 && (v += E.length), v = Math.max(0, Math.min(v - 1, E.length)), T < 0 && (T += E.length), T = Math.max(0, Math.min(T, E.length)), p = E.slice(v, T).join(`
`), h.hasAttribute("data-start") || h.setAttribute("data-start", String(v + 1));
            }
            C.textContent = p, e.highlightElement(C);
          },
          function(p) {
            h.setAttribute(i, _), C.textContent = p;
          }
        );
      }
    }), e.plugins.fileHighlight = {
      /**
       * Executes the File Highlight plugin for all matching `pre` elements under the given container.
       *
       * Note: Elements which are already loaded or currently loading will not be touched by this method.
       *
       * @param {ParentNode} [container=document]
       */
      highlight: function(h) {
        for (var C = (h || document).querySelectorAll(y), c = 0, o; o = C[c++]; )
          e.highlightElement(o);
      }
    };
    var k = !1;
    e.fileHighlight = function() {
      k || (console.warn("Prism.fileHighlight is deprecated. Use `Prism.plugins.fileHighlight.highlight` instead."), k = !0), e.plugins.fileHighlight.highlight.apply(this, arguments);
    };
  }();
})(ut);
var At = ut.exports;
const ze = /* @__PURE__ */ Ft(At);
Prism.languages.python = {
  comment: {
    pattern: /(^|[^\\])#.*/,
    lookbehind: !0,
    greedy: !0
  },
  "string-interpolation": {
    pattern: /(?:f|fr|rf)(?:("""|''')[\s\S]*?\1|("|')(?:\\.|(?!\2)[^\\\r\n])*\2)/i,
    greedy: !0,
    inside: {
      interpolation: {
        // "{" <expression> <optional "!s", "!r", or "!a"> <optional ":" format specifier> "}"
        pattern: /((?:^|[^{])(?:\{\{)*)\{(?!\{)(?:[^{}]|\{(?!\{)(?:[^{}]|\{(?!\{)(?:[^{}])+\})+\})+\}/,
        lookbehind: !0,
        inside: {
          "format-spec": {
            pattern: /(:)[^:(){}]+(?=\}$)/,
            lookbehind: !0
          },
          "conversion-option": {
            pattern: /![sra](?=[:}]$)/,
            alias: "punctuation"
          },
          rest: null
        }
      },
      string: /[\s\S]+/
    }
  },
  "triple-quoted-string": {
    pattern: /(?:[rub]|br|rb)?("""|''')[\s\S]*?\1/i,
    greedy: !0,
    alias: "string"
  },
  string: {
    pattern: /(?:[rub]|br|rb)?("|')(?:\\.|(?!\1)[^\\\r\n])*\1/i,
    greedy: !0
  },
  function: {
    pattern: /((?:^|\s)def[ \t]+)[a-zA-Z_]\w*(?=\s*\()/g,
    lookbehind: !0
  },
  "class-name": {
    pattern: /(\bclass\s+)\w+/i,
    lookbehind: !0
  },
  decorator: {
    pattern: /(^[\t ]*)@\w+(?:\.\w+)*/m,
    lookbehind: !0,
    alias: ["annotation", "punctuation"],
    inside: {
      punctuation: /\./
    }
  },
  keyword: /\b(?:_(?=\s*:)|and|as|assert|async|await|break|case|class|continue|def|del|elif|else|except|exec|finally|for|from|global|if|import|in|is|lambda|match|nonlocal|not|or|pass|print|raise|return|try|while|with|yield)\b/,
  builtin: /\b(?:__import__|abs|all|any|apply|ascii|basestring|bin|bool|buffer|bytearray|bytes|callable|chr|classmethod|cmp|coerce|compile|complex|delattr|dict|dir|divmod|enumerate|eval|execfile|file|filter|float|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|int|intern|isinstance|issubclass|iter|len|list|locals|long|map|max|memoryview|min|next|object|oct|open|ord|pow|property|range|raw_input|reduce|reload|repr|reversed|round|set|setattr|slice|sorted|staticmethod|str|sum|super|tuple|type|unichr|unicode|vars|xrange|zip)\b/,
  boolean: /\b(?:False|None|True)\b/,
  number: /\b0(?:b(?:_?[01])+|o(?:_?[0-7])+|x(?:_?[a-f0-9])+)\b|(?:\b\d+(?:_\d+)*(?:\.(?:\d+(?:_\d+)*)?)?|\B\.\d+(?:_\d+)*)(?:e[+-]?\d+(?:_\d+)*)?j?(?!\w)/i,
  operator: /[-+%=]=?|!=|:=|\*\*?=?|\/\/?=?|<[<=>]?|>[=>]?|[&|^~]/,
  punctuation: /[{}[\];(),.:]/
};
Prism.languages.python["string-interpolation"].inside.interpolation.inside.rest = Prism.languages.python;
Prism.languages.py = Prism.languages.python;
(function(l) {
  l.languages.typescript = l.languages.extend("javascript", {
    "class-name": {
      pattern: /(\b(?:class|extends|implements|instanceof|interface|new|type)\s+)(?!keyof\b)(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*(?:\s*<(?:[^<>]|<(?:[^<>]|<[^<>]*>)*>)*>)?/,
      lookbehind: !0,
      greedy: !0,
      inside: null
      // see below
    },
    builtin: /\b(?:Array|Function|Promise|any|boolean|console|never|number|string|symbol|unknown)\b/
  }), l.languages.typescript.keyword.push(
    /\b(?:abstract|declare|is|keyof|readonly|require)\b/,
    // keywords that have to be followed by an identifier
    /\b(?:asserts|infer|interface|module|namespace|type)\b(?=\s*(?:[{_$a-zA-Z\xA0-\uFFFF]|$))/,
    // This is for `import type *, {}`
    /\btype\b(?=\s*(?:[\{*]|$))/
  ), delete l.languages.typescript.parameter, delete l.languages.typescript["literal-property"];
  var t = l.languages.extend("typescript", {});
  delete t["class-name"], l.languages.typescript["class-name"].inside = t, l.languages.insertBefore("typescript", "function", {
    decorator: {
      pattern: /@[$\w\xA0-\uFFFF]+/,
      inside: {
        at: {
          pattern: /^@/,
          alias: "operator"
        },
        function: /^[\s\S]+/
      }
    },
    "generic-function": {
      // e.g. foo<T extends "bar" | "baz">( ...
      pattern: /#?(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*\s*<(?:[^<>]|<(?:[^<>]|<[^<>]*>)*>)*>(?=\s*\()/,
      greedy: !0,
      inside: {
        function: /^#?(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*/,
        generic: {
          pattern: /<[\s\S]+/,
          // everything after the first <
          alias: "class-name",
          inside: t
        }
      }
    }
  }), l.languages.ts = l.languages.typescript;
})(Prism);
const {
  HtmlTag: ft,
  SvelteComponent: St,
  append: P,
  attr: N,
  binding_callbacks: Et,
  destroy_block: qt,
  detach: $,
  element: B,
  empty: ct,
  ensure_array_like: Me,
  init: Ct,
  insert: ee,
  listen: Lt,
  noop: Pe,
  safe_not_equal: Tt,
  set_data: dt,
  set_style: xt,
  space: ce,
  text: Fe,
  toggle_class: he,
  update_keyed_each: zt
} = window.__gradio__svelte__internal;
function je(l, t, e) {
  const n = l.slice();
  return n[10] = t[e].type, n[11] = t[e].description, n[12] = t[e].default, n[13] = t[e].name, n[14] = t, n[15] = e, n;
}
function De(l) {
  let t = [], e = /* @__PURE__ */ new Map(), n, s = Me(
    /*_docs*/
    l[1]
  );
  const a = (r) => (
    /*name*/
    r[13]
  );
  for (let r = 0; r < s.length; r += 1) {
    let i = je(l, s, r), u = a(i);
    e.set(u, t[r] = Ve(u, i));
  }
  return {
    c() {
      for (let r = 0; r < t.length; r += 1)
        t[r].c();
      n = ct();
    },
    m(r, i) {
      for (let u = 0; u < t.length; u += 1)
        t[u] && t[u].m(r, i);
      ee(r, n, i);
    },
    p(r, i) {
      i & /*show_desc, _docs, lang, el*/
      15 && (s = Me(
        /*_docs*/
        r[1]
      ), t = zt(t, i, a, 1, r, s, e, n.parentNode, qt, Ve, n, je));
    },
    d(r) {
      r && $(n);
      for (let i = 0; i < t.length; i += 1)
        t[i].d(r);
    }
  };
}
function Ze(l) {
  let t, e, n = (
    /*type*/
    l[10] + ""
  ), s;
  return {
    c() {
      t = Fe(": "), e = new ft(!1), s = ct(), e.a = s;
    },
    m(a, r) {
      ee(a, t, r), e.m(n, a, r), ee(a, s, r);
    },
    p(a, r) {
      r & /*_docs*/
      2 && n !== (n = /*type*/
      a[10] + "") && e.p(n);
    },
    d(a) {
      a && ($(t), $(s), e.d());
    }
  };
}
function Ie(l) {
  let t, e, n, s = (
    /*description*/
    l[11] + ""
  ), a, r = (
    /*_default*/
    l[12] && Oe(l)
  );
  return {
    c() {
      r && r.c(), t = ce(), e = B("div"), n = B("p"), a = Fe(s), N(e, "class", "description svelte-xk2x3f");
    },
    m(i, u) {
      r && r.m(i, u), ee(i, t, u), ee(i, e, u), P(e, n), P(n, a);
    },
    p(i, u) {
      /*_default*/
      i[12] ? r ? r.p(i, u) : (r = Oe(i), r.c(), r.m(t.parentNode, t)) : r && (r.d(1), r = null), u & /*_docs*/
      2 && s !== (s = /*description*/
      i[11] + "") && dt(a, s);
    },
    d(i) {
      i && ($(t), $(e)), r && r.d(i);
    }
  };
}
function Oe(l) {
  let t, e, n, s, a, r, i = (
    /*_default*/
    l[12] + ""
  );
  return {
    c() {
      t = B("div"), e = B("span"), e.textContent = "default", n = ce(), s = B("code"), a = Fe("= "), r = new ft(!1), N(e, "class", "svelte-xk2x3f"), xt(e, "padding-right", "4px"), r.a = null, N(s, "class", "svelte-xk2x3f"), N(t, "class", "default svelte-xk2x3f");
    },
    m(u, f) {
      ee(u, t, f), P(t, e), P(t, n), P(t, s), P(s, a), r.m(i, s);
    },
    p(u, f) {
      f & /*_docs*/
      2 && i !== (i = /*_default*/
      u[12] + "") && r.p(i);
    },
    d(u) {
      u && $(t);
    }
  };
}
function Ve(l, t) {
  let e, n, s, a, r = (
    /*name*/
    t[13] + ""
  ), i, u = (
    /*i*/
    t[15]
  ), f, _, y, F, m, k, q, h = (
    /*type*/
    t[10] && Ze(t)
  );
  const C = () => (
    /*code_binding*/
    t[6](a, u)
  ), c = () => (
    /*code_binding*/
    t[6](null, u)
  );
  function o() {
    return (
      /*click_handler*/
      t[7](
        /*i*/
        t[15]
      )
    );
  }
  let d = (
    /*show_desc*/
    t[3][
      /*i*/
      t[15]
    ] && Ie(t)
  );
  return {
    key: l,
    first: null,
    c() {
      e = B("div"), n = B("div"), s = B("pre"), a = B("code"), i = Fe(r), h && h.c(), _ = ce(), y = B("button"), y.textContent = "▲", F = ce(), d && d.c(), m = ce(), N(a, "class", "svelte-xk2x3f"), N(s, "class", f = "language-" + /*lang*/
      t[0] + " svelte-xk2x3f"), N(y, "class", "arrow svelte-xk2x3f"), he(y, "hidden", !/*show_desc*/
      t[3][
        /*i*/
        t[15]
      ]), N(n, "class", "type svelte-xk2x3f"), N(e, "class", "param md svelte-xk2x3f"), he(
        e,
        "open",
        /*show_desc*/
        t[3][
          /*i*/
          t[15]
        ]
      ), this.first = e;
    },
    m(g, p) {
      ee(g, e, p), P(e, n), P(n, s), P(s, a), P(a, i), h && h.m(a, null), C(), P(n, _), P(n, y), P(e, F), d && d.m(e, null), P(e, m), k || (q = Lt(y, "click", o), k = !0);
    },
    p(g, p) {
      t = g, p & /*_docs*/
      2 && r !== (r = /*name*/
      t[13] + "") && dt(i, r), /*type*/
      t[10] ? h ? h.p(t, p) : (h = Ze(t), h.c(), h.m(a, null)) : h && (h.d(1), h = null), u !== /*i*/
      t[15] && (c(), u = /*i*/
      t[15], C()), p & /*lang*/
      1 && f !== (f = "language-" + /*lang*/
      t[0] + " svelte-xk2x3f") && N(s, "class", f), p & /*show_desc, _docs*/
      10 && he(y, "hidden", !/*show_desc*/
      t[3][
        /*i*/
        t[15]
      ]), /*show_desc*/
      t[3][
        /*i*/
        t[15]
      ] ? d ? d.p(t, p) : (d = Ie(t), d.c(), d.m(e, m)) : d && (d.d(1), d = null), p & /*show_desc, _docs*/
      10 && he(
        e,
        "open",
        /*show_desc*/
        t[3][
          /*i*/
          t[15]
        ]
      );
    },
    d(g) {
      g && $(e), h && h.d(), c(), d && d.d(), k = !1, q();
    }
  };
}
function Mt(l) {
  let t, e = (
    /*_docs*/
    l[1] && De(l)
  );
  return {
    c() {
      t = B("div"), e && e.c(), N(t, "class", "wrap svelte-xk2x3f");
    },
    m(n, s) {
      ee(n, t, s), e && e.m(t, null);
    },
    p(n, [s]) {
      /*_docs*/
      n[1] ? e ? e.p(n, s) : (e = De(n), e.c(), e.m(t, null)) : e && (e.d(1), e = null);
    },
    i: Pe,
    o: Pe,
    d(n) {
      n && $(t), e && e.d();
    }
  };
}
function Pt(l, t, e) {
  let n, { docs: s } = t, { lang: a = "python" } = t, { linkify: r = [] } = t, i;
  function u(m, k) {
    let q = ze.highlight(m, ze.languages[k], k);
    for (const h of r)
      q = q.replace(new RegExp(h, "g"), `<a href="#h-${h.toLocaleLowerCase()}">${h}</a>`);
    return q;
  }
  function f(m, k) {
    return Object.entries(m).map(([q, { type: h, description: C, default: c }]) => {
      let o = h ? u(h, k) : null;
      return {
        name: q,
        type: o,
        description: C,
        default: c ? u(c, k) : null
      };
    });
  }
  let _ = [];
  function y(m, k) {
    Et[m ? "unshift" : "push"](() => {
      _[k] = m, e(2, _);
    });
  }
  const F = (m) => e(3, n[m] = !n[m], n);
  return l.$$set = (m) => {
    "docs" in m && e(4, s = m.docs), "lang" in m && e(0, a = m.lang), "linkify" in m && e(5, r = m.linkify);
  }, l.$$.update = () => {
    l.$$.dirty & /*docs, lang*/
    17 && setTimeout(
      () => {
        e(1, i = f(s, a));
      },
      0
    ), l.$$.dirty & /*_docs*/
    2 && e(3, n = i && i.map((m) => !1));
  }, [a, i, _, n, s, r, y, F];
}
class jt extends St {
  constructor(t) {
    super(), Ct(this, t, Pt, Mt, Tt, { docs: 4, lang: 0, linkify: 5 });
  }
}
function ie(l) {
  let t = ["", "k", "M", "G", "T", "P", "E", "Z"], e = 0;
  for (; l > 1e3 && e < t.length - 1; )
    l /= 1e3, e++;
  let n = t[e];
  return (Number.isInteger(l) ? l : l.toFixed(1)) + n;
}
function ye() {
}
function Dt(l, t) {
  return l != l ? t == t : l !== t || l && typeof l == "object" || typeof l == "function";
}
const gt = typeof window < "u";
let Re = gt ? () => window.performance.now() : () => Date.now(), _t = gt ? (l) => requestAnimationFrame(l) : ye;
const se = /* @__PURE__ */ new Set();
function pt(l) {
  se.forEach((t) => {
    t.c(l) || (se.delete(t), t.f());
  }), se.size !== 0 && _t(pt);
}
function Zt(l) {
  let t;
  return se.size === 0 && _t(pt), {
    promise: new Promise((e) => {
      se.add(t = { c: l, f: e });
    }),
    abort() {
      se.delete(t);
    }
  };
}
const le = [];
function It(l, t = ye) {
  let e;
  const n = /* @__PURE__ */ new Set();
  function s(i) {
    if (Dt(l, i) && (l = i, e)) {
      const u = !le.length;
      for (const f of n)
        f[1](), le.push(f, l);
      if (u) {
        for (let f = 0; f < le.length; f += 2)
          le[f][0](le[f + 1]);
        le.length = 0;
      }
    }
  }
  function a(i) {
    s(i(l));
  }
  function r(i, u = ye) {
    const f = [i, u];
    return n.add(f), n.size === 1 && (e = t(s, a) || ye), i(l), () => {
      n.delete(f), n.size === 0 && e && (e(), e = null);
    };
  }
  return { set: s, update: a, subscribe: r };
}
function Ne(l) {
  return Object.prototype.toString.call(l) === "[object Date]";
}
function Ce(l, t, e, n) {
  if (typeof e == "number" || Ne(e)) {
    const s = n - e, a = (e - t) / (l.dt || 1 / 60), r = l.opts.stiffness * s, i = l.opts.damping * a, u = (r - i) * l.inv_mass, f = (a + u) * l.dt;
    return Math.abs(f) < l.opts.precision && Math.abs(s) < l.opts.precision ? n : (l.settled = !1, Ne(e) ? new Date(e.getTime() + f) : e + f);
  } else {
    if (Array.isArray(e))
      return e.map(
        (s, a) => Ce(l, t[a], e[a], n[a])
      );
    if (typeof e == "object") {
      const s = {};
      for (const a in e)
        s[a] = Ce(l, t[a], e[a], n[a]);
      return s;
    } else
      throw new Error(`Cannot spring ${typeof e} values`);
  }
}
function Be(l, t = {}) {
  const e = It(l), { stiffness: n = 0.15, damping: s = 0.8, precision: a = 0.01 } = t;
  let r, i, u, f = l, _ = l, y = 1, F = 0, m = !1;
  function k(h, C = {}) {
    _ = h;
    const c = u = {};
    return l == null || C.hard || q.stiffness >= 1 && q.damping >= 1 ? (m = !0, r = Re(), f = h, e.set(l = _), Promise.resolve()) : (C.soft && (F = 1 / ((C.soft === !0 ? 0.5 : +C.soft) * 60), y = 0), i || (r = Re(), m = !1, i = Zt((o) => {
      if (m)
        return m = !1, i = null, !1;
      y = Math.min(y + F, 1);
      const d = {
        inv_mass: y,
        opts: q,
        settled: !0,
        dt: (o - r) * 60 / 1e3
      }, g = Ce(d, f, l, _);
      return r = o, f = l, e.set(l = g), d.settled && (i = null), !d.settled;
    })), new Promise((o) => {
      i.promise.then(() => {
        c === u && o();
      });
    }));
  }
  const q = {
    set: k,
    update: (h, C) => k(h(_, l), C),
    subscribe: e.subscribe,
    stiffness: n,
    damping: s,
    precision: a
  };
  return q;
}
const {
  SvelteComponent: Ot,
  append: V,
  attr: L,
  component_subscribe: Ge,
  detach: Vt,
  element: Rt,
  init: Nt,
  insert: Bt,
  noop: He,
  safe_not_equal: Gt,
  set_style: be,
  svg_element: R,
  toggle_class: Ue
} = window.__gradio__svelte__internal, { onMount: Ht } = window.__gradio__svelte__internal;
function Ut(l) {
  let t, e, n, s, a, r, i, u, f, _, y, F;
  return {
    c() {
      t = Rt("div"), e = R("svg"), n = R("g"), s = R("path"), a = R("path"), r = R("path"), i = R("path"), u = R("g"), f = R("path"), _ = R("path"), y = R("path"), F = R("path"), L(s, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), L(s, "fill", "#FF7C00"), L(s, "fill-opacity", "0.4"), L(s, "class", "svelte-43sxxs"), L(a, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), L(a, "fill", "#FF7C00"), L(a, "class", "svelte-43sxxs"), L(r, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), L(r, "fill", "#FF7C00"), L(r, "fill-opacity", "0.4"), L(r, "class", "svelte-43sxxs"), L(i, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), L(i, "fill", "#FF7C00"), L(i, "class", "svelte-43sxxs"), be(n, "transform", "translate(" + /*$top*/
      l[1][0] + "px, " + /*$top*/
      l[1][1] + "px)"), L(f, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), L(f, "fill", "#FF7C00"), L(f, "fill-opacity", "0.4"), L(f, "class", "svelte-43sxxs"), L(_, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), L(_, "fill", "#FF7C00"), L(_, "class", "svelte-43sxxs"), L(y, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), L(y, "fill", "#FF7C00"), L(y, "fill-opacity", "0.4"), L(y, "class", "svelte-43sxxs"), L(F, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), L(F, "fill", "#FF7C00"), L(F, "class", "svelte-43sxxs"), be(u, "transform", "translate(" + /*$bottom*/
      l[2][0] + "px, " + /*$bottom*/
      l[2][1] + "px)"), L(e, "viewBox", "-1200 -1200 3000 3000"), L(e, "fill", "none"), L(e, "xmlns", "http://www.w3.org/2000/svg"), L(e, "class", "svelte-43sxxs"), L(t, "class", "svelte-43sxxs"), Ue(
        t,
        "margin",
        /*margin*/
        l[0]
      );
    },
    m(m, k) {
      Bt(m, t, k), V(t, e), V(e, n), V(n, s), V(n, a), V(n, r), V(n, i), V(e, u), V(u, f), V(u, _), V(u, y), V(u, F);
    },
    p(m, [k]) {
      k & /*$top*/
      2 && be(n, "transform", "translate(" + /*$top*/
      m[1][0] + "px, " + /*$top*/
      m[1][1] + "px)"), k & /*$bottom*/
      4 && be(u, "transform", "translate(" + /*$bottom*/
      m[2][0] + "px, " + /*$bottom*/
      m[2][1] + "px)"), k & /*margin*/
      1 && Ue(
        t,
        "margin",
        /*margin*/
        m[0]
      );
    },
    i: He,
    o: He,
    d(m) {
      m && Vt(t);
    }
  };
}
function Wt(l, t, e) {
  let n, s, { margin: a = !0 } = t;
  const r = Be([0, 0]);
  Ge(l, r, (F) => e(1, n = F));
  const i = Be([0, 0]);
  Ge(l, i, (F) => e(2, s = F));
  let u;
  async function f() {
    await Promise.all([r.set([125, 140]), i.set([-125, -140])]), await Promise.all([r.set([-125, 140]), i.set([125, -140])]), await Promise.all([r.set([-125, 0]), i.set([125, -0])]), await Promise.all([r.set([125, 0]), i.set([-125, 0])]);
  }
  async function _() {
    await f(), u || _();
  }
  async function y() {
    await Promise.all([r.set([125, 0]), i.set([-125, 0])]), _();
  }
  return Ht(() => (y(), () => u = !0)), l.$$set = (F) => {
    "margin" in F && e(0, a = F.margin);
  }, [a, n, s, r, i];
}
class Xt extends Ot {
  constructor(t) {
    super(), Nt(this, t, Wt, Ut, Gt, { margin: 0 });
  }
}
const {
  SvelteComponent: Yt,
  append: te,
  attr: U,
  binding_callbacks: We,
  check_outros: mt,
  create_component: Jt,
  create_slot: Kt,
  destroy_component: Qt,
  destroy_each: ht,
  detach: A,
  element: Y,
  empty: oe,
  ensure_array_like: ke,
  get_all_dirty_from_scope: $t,
  get_slot_changes: en,
  group_outros: bt,
  init: tn,
  insert: S,
  mount_component: nn,
  noop: Le,
  safe_not_equal: ln,
  set_data: I,
  set_style: Q,
  space: W,
  text: x,
  toggle_class: Z,
  transition_in: re,
  transition_out: ae,
  update_slot_base: sn
} = window.__gradio__svelte__internal, { tick: rn } = window.__gradio__svelte__internal, { onDestroy: an } = window.__gradio__svelte__internal, on = (l) => ({}), Xe = (l) => ({});
function Ye(l, t, e) {
  const n = l.slice();
  return n[38] = t[e], n[40] = e, n;
}
function Je(l, t, e) {
  const n = l.slice();
  return n[38] = t[e], n;
}
function un(l) {
  let t, e = (
    /*i18n*/
    l[1]("common.error") + ""
  ), n, s, a;
  const r = (
    /*#slots*/
    l[29].error
  ), i = Kt(
    r,
    l,
    /*$$scope*/
    l[28],
    Xe
  );
  return {
    c() {
      t = Y("span"), n = x(e), s = W(), i && i.c(), U(t, "class", "error svelte-1txqlrd");
    },
    m(u, f) {
      S(u, t, f), te(t, n), S(u, s, f), i && i.m(u, f), a = !0;
    },
    p(u, f) {
      (!a || f[0] & /*i18n*/
      2) && e !== (e = /*i18n*/
      u[1]("common.error") + "") && I(n, e), i && i.p && (!a || f[0] & /*$$scope*/
      268435456) && sn(
        i,
        r,
        u,
        /*$$scope*/
        u[28],
        a ? en(
          r,
          /*$$scope*/
          u[28],
          f,
          on
        ) : $t(
          /*$$scope*/
          u[28]
        ),
        Xe
      );
    },
    i(u) {
      a || (re(i, u), a = !0);
    },
    o(u) {
      ae(i, u), a = !1;
    },
    d(u) {
      u && (A(t), A(s)), i && i.d(u);
    }
  };
}
function fn(l) {
  let t, e, n, s, a, r, i, u, f, _ = (
    /*variant*/
    l[8] === "default" && /*show_eta_bar*/
    l[18] && /*show_progress*/
    l[6] === "full" && Ke(l)
  );
  function y(o, d) {
    if (
      /*progress*/
      o[7]
    )
      return gn;
    if (
      /*queue_position*/
      o[2] !== null && /*queue_size*/
      o[3] !== void 0 && /*queue_position*/
      o[2] >= 0
    )
      return dn;
    if (
      /*queue_position*/
      o[2] === 0
    )
      return cn;
  }
  let F = y(l), m = F && F(l), k = (
    /*timer*/
    l[5] && et(l)
  );
  const q = [hn, mn], h = [];
  function C(o, d) {
    return (
      /*last_progress_level*/
      o[15] != null ? 0 : (
        /*show_progress*/
        o[6] === "full" ? 1 : -1
      )
    );
  }
  ~(a = C(l)) && (r = h[a] = q[a](l));
  let c = !/*timer*/
  l[5] && at(l);
  return {
    c() {
      _ && _.c(), t = W(), e = Y("div"), m && m.c(), n = W(), k && k.c(), s = W(), r && r.c(), i = W(), c && c.c(), u = oe(), U(e, "class", "progress-text svelte-1txqlrd"), Z(
        e,
        "meta-text-center",
        /*variant*/
        l[8] === "center"
      ), Z(
        e,
        "meta-text",
        /*variant*/
        l[8] === "default"
      );
    },
    m(o, d) {
      _ && _.m(o, d), S(o, t, d), S(o, e, d), m && m.m(e, null), te(e, n), k && k.m(e, null), S(o, s, d), ~a && h[a].m(o, d), S(o, i, d), c && c.m(o, d), S(o, u, d), f = !0;
    },
    p(o, d) {
      /*variant*/
      o[8] === "default" && /*show_eta_bar*/
      o[18] && /*show_progress*/
      o[6] === "full" ? _ ? _.p(o, d) : (_ = Ke(o), _.c(), _.m(t.parentNode, t)) : _ && (_.d(1), _ = null), F === (F = y(o)) && m ? m.p(o, d) : (m && m.d(1), m = F && F(o), m && (m.c(), m.m(e, n))), /*timer*/
      o[5] ? k ? k.p(o, d) : (k = et(o), k.c(), k.m(e, null)) : k && (k.d(1), k = null), (!f || d[0] & /*variant*/
      256) && Z(
        e,
        "meta-text-center",
        /*variant*/
        o[8] === "center"
      ), (!f || d[0] & /*variant*/
      256) && Z(
        e,
        "meta-text",
        /*variant*/
        o[8] === "default"
      );
      let g = a;
      a = C(o), a === g ? ~a && h[a].p(o, d) : (r && (bt(), ae(h[g], 1, 1, () => {
        h[g] = null;
      }), mt()), ~a ? (r = h[a], r ? r.p(o, d) : (r = h[a] = q[a](o), r.c()), re(r, 1), r.m(i.parentNode, i)) : r = null), /*timer*/
      o[5] ? c && (c.d(1), c = null) : c ? c.p(o, d) : (c = at(o), c.c(), c.m(u.parentNode, u));
    },
    i(o) {
      f || (re(r), f = !0);
    },
    o(o) {
      ae(r), f = !1;
    },
    d(o) {
      o && (A(t), A(e), A(s), A(i), A(u)), _ && _.d(o), m && m.d(), k && k.d(), ~a && h[a].d(o), c && c.d(o);
    }
  };
}
function Ke(l) {
  let t, e = `translateX(${/*eta_level*/
  (l[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      t = Y("div"), U(t, "class", "eta-bar svelte-1txqlrd"), Q(t, "transform", e);
    },
    m(n, s) {
      S(n, t, s);
    },
    p(n, s) {
      s[0] & /*eta_level*/
      131072 && e !== (e = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && Q(t, "transform", e);
    },
    d(n) {
      n && A(t);
    }
  };
}
function cn(l) {
  let t;
  return {
    c() {
      t = x("processing |");
    },
    m(e, n) {
      S(e, t, n);
    },
    p: Le,
    d(e) {
      e && A(t);
    }
  };
}
function dn(l) {
  let t, e = (
    /*queue_position*/
    l[2] + 1 + ""
  ), n, s, a, r;
  return {
    c() {
      t = x("queue: "), n = x(e), s = x("/"), a = x(
        /*queue_size*/
        l[3]
      ), r = x(" |");
    },
    m(i, u) {
      S(i, t, u), S(i, n, u), S(i, s, u), S(i, a, u), S(i, r, u);
    },
    p(i, u) {
      u[0] & /*queue_position*/
      4 && e !== (e = /*queue_position*/
      i[2] + 1 + "") && I(n, e), u[0] & /*queue_size*/
      8 && I(
        a,
        /*queue_size*/
        i[3]
      );
    },
    d(i) {
      i && (A(t), A(n), A(s), A(a), A(r));
    }
  };
}
function gn(l) {
  let t, e = ke(
    /*progress*/
    l[7]
  ), n = [];
  for (let s = 0; s < e.length; s += 1)
    n[s] = $e(Je(l, e, s));
  return {
    c() {
      for (let s = 0; s < n.length; s += 1)
        n[s].c();
      t = oe();
    },
    m(s, a) {
      for (let r = 0; r < n.length; r += 1)
        n[r] && n[r].m(s, a);
      S(s, t, a);
    },
    p(s, a) {
      if (a[0] & /*progress*/
      128) {
        e = ke(
          /*progress*/
          s[7]
        );
        let r;
        for (r = 0; r < e.length; r += 1) {
          const i = Je(s, e, r);
          n[r] ? n[r].p(i, a) : (n[r] = $e(i), n[r].c(), n[r].m(t.parentNode, t));
        }
        for (; r < n.length; r += 1)
          n[r].d(1);
        n.length = e.length;
      }
    },
    d(s) {
      s && A(t), ht(n, s);
    }
  };
}
function Qe(l) {
  let t, e = (
    /*p*/
    l[38].unit + ""
  ), n, s, a = " ", r;
  function i(_, y) {
    return (
      /*p*/
      _[38].length != null ? pn : _n
    );
  }
  let u = i(l), f = u(l);
  return {
    c() {
      f.c(), t = W(), n = x(e), s = x(" | "), r = x(a);
    },
    m(_, y) {
      f.m(_, y), S(_, t, y), S(_, n, y), S(_, s, y), S(_, r, y);
    },
    p(_, y) {
      u === (u = i(_)) && f ? f.p(_, y) : (f.d(1), f = u(_), f && (f.c(), f.m(t.parentNode, t))), y[0] & /*progress*/
      128 && e !== (e = /*p*/
      _[38].unit + "") && I(n, e);
    },
    d(_) {
      _ && (A(t), A(n), A(s), A(r)), f.d(_);
    }
  };
}
function _n(l) {
  let t = ie(
    /*p*/
    l[38].index || 0
  ) + "", e;
  return {
    c() {
      e = x(t);
    },
    m(n, s) {
      S(n, e, s);
    },
    p(n, s) {
      s[0] & /*progress*/
      128 && t !== (t = ie(
        /*p*/
        n[38].index || 0
      ) + "") && I(e, t);
    },
    d(n) {
      n && A(e);
    }
  };
}
function pn(l) {
  let t = ie(
    /*p*/
    l[38].index || 0
  ) + "", e, n, s = ie(
    /*p*/
    l[38].length
  ) + "", a;
  return {
    c() {
      e = x(t), n = x("/"), a = x(s);
    },
    m(r, i) {
      S(r, e, i), S(r, n, i), S(r, a, i);
    },
    p(r, i) {
      i[0] & /*progress*/
      128 && t !== (t = ie(
        /*p*/
        r[38].index || 0
      ) + "") && I(e, t), i[0] & /*progress*/
      128 && s !== (s = ie(
        /*p*/
        r[38].length
      ) + "") && I(a, s);
    },
    d(r) {
      r && (A(e), A(n), A(a));
    }
  };
}
function $e(l) {
  let t, e = (
    /*p*/
    l[38].index != null && Qe(l)
  );
  return {
    c() {
      e && e.c(), t = oe();
    },
    m(n, s) {
      e && e.m(n, s), S(n, t, s);
    },
    p(n, s) {
      /*p*/
      n[38].index != null ? e ? e.p(n, s) : (e = Qe(n), e.c(), e.m(t.parentNode, t)) : e && (e.d(1), e = null);
    },
    d(n) {
      n && A(t), e && e.d(n);
    }
  };
}
function et(l) {
  let t, e = (
    /*eta*/
    l[0] ? `/${/*formatted_eta*/
    l[19]}` : ""
  ), n, s;
  return {
    c() {
      t = x(
        /*formatted_timer*/
        l[20]
      ), n = x(e), s = x("s");
    },
    m(a, r) {
      S(a, t, r), S(a, n, r), S(a, s, r);
    },
    p(a, r) {
      r[0] & /*formatted_timer*/
      1048576 && I(
        t,
        /*formatted_timer*/
        a[20]
      ), r[0] & /*eta, formatted_eta*/
      524289 && e !== (e = /*eta*/
      a[0] ? `/${/*formatted_eta*/
      a[19]}` : "") && I(n, e);
    },
    d(a) {
      a && (A(t), A(n), A(s));
    }
  };
}
function mn(l) {
  let t, e;
  return t = new Xt({
    props: { margin: (
      /*variant*/
      l[8] === "default"
    ) }
  }), {
    c() {
      Jt(t.$$.fragment);
    },
    m(n, s) {
      nn(t, n, s), e = !0;
    },
    p(n, s) {
      const a = {};
      s[0] & /*variant*/
      256 && (a.margin = /*variant*/
      n[8] === "default"), t.$set(a);
    },
    i(n) {
      e || (re(t.$$.fragment, n), e = !0);
    },
    o(n) {
      ae(t.$$.fragment, n), e = !1;
    },
    d(n) {
      Qt(t, n);
    }
  };
}
function hn(l) {
  let t, e, n, s, a, r = `${/*last_progress_level*/
  l[15] * 100}%`, i = (
    /*progress*/
    l[7] != null && tt(l)
  );
  return {
    c() {
      t = Y("div"), e = Y("div"), i && i.c(), n = W(), s = Y("div"), a = Y("div"), U(e, "class", "progress-level-inner svelte-1txqlrd"), U(a, "class", "progress-bar svelte-1txqlrd"), Q(a, "width", r), U(s, "class", "progress-bar-wrap svelte-1txqlrd"), U(t, "class", "progress-level svelte-1txqlrd");
    },
    m(u, f) {
      S(u, t, f), te(t, e), i && i.m(e, null), te(t, n), te(t, s), te(s, a), l[30](a);
    },
    p(u, f) {
      /*progress*/
      u[7] != null ? i ? i.p(u, f) : (i = tt(u), i.c(), i.m(e, null)) : i && (i.d(1), i = null), f[0] & /*last_progress_level*/
      32768 && r !== (r = `${/*last_progress_level*/
      u[15] * 100}%`) && Q(a, "width", r);
    },
    i: Le,
    o: Le,
    d(u) {
      u && A(t), i && i.d(), l[30](null);
    }
  };
}
function tt(l) {
  let t, e = ke(
    /*progress*/
    l[7]
  ), n = [];
  for (let s = 0; s < e.length; s += 1)
    n[s] = rt(Ye(l, e, s));
  return {
    c() {
      for (let s = 0; s < n.length; s += 1)
        n[s].c();
      t = oe();
    },
    m(s, a) {
      for (let r = 0; r < n.length; r += 1)
        n[r] && n[r].m(s, a);
      S(s, t, a);
    },
    p(s, a) {
      if (a[0] & /*progress_level, progress*/
      16512) {
        e = ke(
          /*progress*/
          s[7]
        );
        let r;
        for (r = 0; r < e.length; r += 1) {
          const i = Ye(s, e, r);
          n[r] ? n[r].p(i, a) : (n[r] = rt(i), n[r].c(), n[r].m(t.parentNode, t));
        }
        for (; r < n.length; r += 1)
          n[r].d(1);
        n.length = e.length;
      }
    },
    d(s) {
      s && A(t), ht(n, s);
    }
  };
}
function nt(l) {
  let t, e, n, s, a = (
    /*i*/
    l[40] !== 0 && bn()
  ), r = (
    /*p*/
    l[38].desc != null && lt(l)
  ), i = (
    /*p*/
    l[38].desc != null && /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[40]
    ] != null && it()
  ), u = (
    /*progress_level*/
    l[14] != null && st(l)
  );
  return {
    c() {
      a && a.c(), t = W(), r && r.c(), e = W(), i && i.c(), n = W(), u && u.c(), s = oe();
    },
    m(f, _) {
      a && a.m(f, _), S(f, t, _), r && r.m(f, _), S(f, e, _), i && i.m(f, _), S(f, n, _), u && u.m(f, _), S(f, s, _);
    },
    p(f, _) {
      /*p*/
      f[38].desc != null ? r ? r.p(f, _) : (r = lt(f), r.c(), r.m(e.parentNode, e)) : r && (r.d(1), r = null), /*p*/
      f[38].desc != null && /*progress_level*/
      f[14] && /*progress_level*/
      f[14][
        /*i*/
        f[40]
      ] != null ? i || (i = it(), i.c(), i.m(n.parentNode, n)) : i && (i.d(1), i = null), /*progress_level*/
      f[14] != null ? u ? u.p(f, _) : (u = st(f), u.c(), u.m(s.parentNode, s)) : u && (u.d(1), u = null);
    },
    d(f) {
      f && (A(t), A(e), A(n), A(s)), a && a.d(f), r && r.d(f), i && i.d(f), u && u.d(f);
    }
  };
}
function bn(l) {
  let t;
  return {
    c() {
      t = x(" /");
    },
    m(e, n) {
      S(e, t, n);
    },
    d(e) {
      e && A(t);
    }
  };
}
function lt(l) {
  let t = (
    /*p*/
    l[38].desc + ""
  ), e;
  return {
    c() {
      e = x(t);
    },
    m(n, s) {
      S(n, e, s);
    },
    p(n, s) {
      s[0] & /*progress*/
      128 && t !== (t = /*p*/
      n[38].desc + "") && I(e, t);
    },
    d(n) {
      n && A(e);
    }
  };
}
function it(l) {
  let t;
  return {
    c() {
      t = x("-");
    },
    m(e, n) {
      S(e, t, n);
    },
    d(e) {
      e && A(t);
    }
  };
}
function st(l) {
  let t = (100 * /*progress_level*/
  (l[14][
    /*i*/
    l[40]
  ] || 0)).toFixed(1) + "", e, n;
  return {
    c() {
      e = x(t), n = x("%");
    },
    m(s, a) {
      S(s, e, a), S(s, n, a);
    },
    p(s, a) {
      a[0] & /*progress_level*/
      16384 && t !== (t = (100 * /*progress_level*/
      (s[14][
        /*i*/
        s[40]
      ] || 0)).toFixed(1) + "") && I(e, t);
    },
    d(s) {
      s && (A(e), A(n));
    }
  };
}
function rt(l) {
  let t, e = (
    /*p*/
    (l[38].desc != null || /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[40]
    ] != null) && nt(l)
  );
  return {
    c() {
      e && e.c(), t = oe();
    },
    m(n, s) {
      e && e.m(n, s), S(n, t, s);
    },
    p(n, s) {
      /*p*/
      n[38].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[40]
      ] != null ? e ? e.p(n, s) : (e = nt(n), e.c(), e.m(t.parentNode, t)) : e && (e.d(1), e = null);
    },
    d(n) {
      n && A(t), e && e.d(n);
    }
  };
}
function at(l) {
  let t, e;
  return {
    c() {
      t = Y("p"), e = x(
        /*loading_text*/
        l[9]
      ), U(t, "class", "loading svelte-1txqlrd");
    },
    m(n, s) {
      S(n, t, s), te(t, e);
    },
    p(n, s) {
      s[0] & /*loading_text*/
      512 && I(
        e,
        /*loading_text*/
        n[9]
      );
    },
    d(n) {
      n && A(t);
    }
  };
}
function vn(l) {
  let t, e, n, s, a;
  const r = [fn, un], i = [];
  function u(f, _) {
    return (
      /*status*/
      f[4] === "pending" ? 0 : (
        /*status*/
        f[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(e = u(l)) && (n = i[e] = r[e](l)), {
    c() {
      t = Y("div"), n && n.c(), U(t, "class", s = "wrap " + /*variant*/
      l[8] + " " + /*show_progress*/
      l[6] + " svelte-1txqlrd"), Z(t, "hide", !/*status*/
      l[4] || /*status*/
      l[4] === "complete" || /*show_progress*/
      l[6] === "hidden"), Z(
        t,
        "translucent",
        /*variant*/
        l[8] === "center" && /*status*/
        (l[4] === "pending" || /*status*/
        l[4] === "error") || /*translucent*/
        l[11] || /*show_progress*/
        l[6] === "minimal"
      ), Z(
        t,
        "generating",
        /*status*/
        l[4] === "generating"
      ), Z(
        t,
        "border",
        /*border*/
        l[12]
      ), Q(
        t,
        "position",
        /*absolute*/
        l[10] ? "absolute" : "static"
      ), Q(
        t,
        "padding",
        /*absolute*/
        l[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(f, _) {
      S(f, t, _), ~e && i[e].m(t, null), l[31](t), a = !0;
    },
    p(f, _) {
      let y = e;
      e = u(f), e === y ? ~e && i[e].p(f, _) : (n && (bt(), ae(i[y], 1, 1, () => {
        i[y] = null;
      }), mt()), ~e ? (n = i[e], n ? n.p(f, _) : (n = i[e] = r[e](f), n.c()), re(n, 1), n.m(t, null)) : n = null), (!a || _[0] & /*variant, show_progress*/
      320 && s !== (s = "wrap " + /*variant*/
      f[8] + " " + /*show_progress*/
      f[6] + " svelte-1txqlrd")) && U(t, "class", s), (!a || _[0] & /*variant, show_progress, status, show_progress*/
      336) && Z(t, "hide", !/*status*/
      f[4] || /*status*/
      f[4] === "complete" || /*show_progress*/
      f[6] === "hidden"), (!a || _[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && Z(
        t,
        "translucent",
        /*variant*/
        f[8] === "center" && /*status*/
        (f[4] === "pending" || /*status*/
        f[4] === "error") || /*translucent*/
        f[11] || /*show_progress*/
        f[6] === "minimal"
      ), (!a || _[0] & /*variant, show_progress, status*/
      336) && Z(
        t,
        "generating",
        /*status*/
        f[4] === "generating"
      ), (!a || _[0] & /*variant, show_progress, border*/
      4416) && Z(
        t,
        "border",
        /*border*/
        f[12]
      ), _[0] & /*absolute*/
      1024 && Q(
        t,
        "position",
        /*absolute*/
        f[10] ? "absolute" : "static"
      ), _[0] & /*absolute*/
      1024 && Q(
        t,
        "padding",
        /*absolute*/
        f[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(f) {
      a || (re(n), a = !0);
    },
    o(f) {
      ae(n), a = !1;
    },
    d(f) {
      f && A(t), ~e && i[e].d(), l[31](null);
    }
  };
}
let ve = [], qe = !1;
async function yn(l, t = !0) {
  if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
    if (ve.push(l), !qe)
      qe = !0;
    else
      return;
    await rn(), requestAnimationFrame(() => {
      let e = [0, 0];
      for (let n = 0; n < ve.length; n++) {
        const a = ve[n].getBoundingClientRect();
        (n === 0 || a.top + window.scrollY <= e[0]) && (e[0] = a.top + window.scrollY, e[1] = n);
      }
      window.scrollTo({ top: e[0] - 20, behavior: "smooth" }), qe = !1, ve = [];
    });
  }
}
function wn(l, t, e) {
  let n, { $$slots: s = {}, $$scope: a } = t, { i18n: r } = t, { eta: i = null } = t, { queue: u = !1 } = t, { queue_position: f } = t, { queue_size: _ } = t, { status: y } = t, { scroll_to_output: F = !1 } = t, { timer: m = !0 } = t, { show_progress: k = "full" } = t, { message: q = null } = t, { progress: h = null } = t, { variant: C = "default" } = t, { loading_text: c = "Loading..." } = t, { absolute: o = !0 } = t, { translucent: d = !1 } = t, { border: g = !1 } = t, { autoscroll: p } = t, b, E = !1, v = 0, T = 0, z = null, O = 0, G = null, J, H = null, de = !0;
  const ge = () => {
    e(25, v = performance.now()), e(26, T = 0), E = !0, M();
  };
  function M() {
    requestAnimationFrame(() => {
      e(26, T = (performance.now() - v) / 1e3), E && M();
    });
  }
  function j() {
    e(26, T = 0), E && (E = !1);
  }
  an(() => {
    E && j();
  });
  let X = null;
  function ne(w) {
    We[w ? "unshift" : "push"](() => {
      H = w, e(16, H), e(7, h), e(14, G), e(15, J);
    });
  }
  function D(w) {
    We[w ? "unshift" : "push"](() => {
      b = w, e(13, b);
    });
  }
  return l.$$set = (w) => {
    "i18n" in w && e(1, r = w.i18n), "eta" in w && e(0, i = w.eta), "queue" in w && e(21, u = w.queue), "queue_position" in w && e(2, f = w.queue_position), "queue_size" in w && e(3, _ = w.queue_size), "status" in w && e(4, y = w.status), "scroll_to_output" in w && e(22, F = w.scroll_to_output), "timer" in w && e(5, m = w.timer), "show_progress" in w && e(6, k = w.show_progress), "message" in w && e(23, q = w.message), "progress" in w && e(7, h = w.progress), "variant" in w && e(8, C = w.variant), "loading_text" in w && e(9, c = w.loading_text), "absolute" in w && e(10, o = w.absolute), "translucent" in w && e(11, d = w.translucent), "border" in w && e(12, g = w.border), "autoscroll" in w && e(24, p = w.autoscroll), "$$scope" in w && e(28, a = w.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*eta, old_eta, queue, timer_start*/
    169869313 && (i === null ? e(0, i = z) : u && e(0, i = (performance.now() - v) / 1e3 + i), i != null && (e(19, X = i.toFixed(1)), e(27, z = i))), l.$$.dirty[0] & /*eta, timer_diff*/
    67108865 && e(17, O = i === null || i <= 0 || !T ? null : Math.min(T / i, 1)), l.$$.dirty[0] & /*progress*/
    128 && h != null && e(18, de = !1), l.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (h != null ? e(14, G = h.map((w) => {
      if (w.index != null && w.length != null)
        return w.index / w.length;
      if (w.progress != null)
        return w.progress;
    })) : e(14, G = null), G ? (e(15, J = G[G.length - 1]), H && (J === 0 ? e(16, H.style.transition = "0", H) : e(16, H.style.transition = "150ms", H))) : e(15, J = void 0)), l.$$.dirty[0] & /*status*/
    16 && (y === "pending" ? ge() : j()), l.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && b && F && (y === "pending" || y === "complete") && yn(b, p), l.$$.dirty[0] & /*status, message*/
    8388624, l.$$.dirty[0] & /*timer_diff*/
    67108864 && e(20, n = T.toFixed(1));
  }, [
    i,
    r,
    f,
    _,
    y,
    m,
    k,
    h,
    C,
    c,
    o,
    d,
    g,
    b,
    G,
    J,
    H,
    O,
    de,
    X,
    n,
    u,
    F,
    q,
    p,
    v,
    T,
    z,
    a,
    s,
    ne,
    D
  ];
}
class kn extends Yt {
  constructor(t) {
    super(), tn(
      this,
      t,
      wn,
      vn,
      ln,
      {
        i18n: 1,
        eta: 0,
        queue: 21,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: Fn,
  assign: An,
  check_outros: Sn,
  create_component: vt,
  destroy_component: yt,
  detach: En,
  get_spread_object: qn,
  get_spread_update: Cn,
  group_outros: Ln,
  init: Tn,
  insert: xn,
  mount_component: wt,
  safe_not_equal: zn,
  space: Mn,
  transition_in: fe,
  transition_out: we
} = window.__gradio__svelte__internal;
function ot(l) {
  let t, e;
  const n = [
    { autoscroll: (
      /*gradio*/
      l[2].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      l[2].i18n
    ) },
    /*loading_status*/
    l[1]
  ];
  let s = {};
  for (let a = 0; a < n.length; a += 1)
    s = An(s, n[a]);
  return t = new kn({ props: s }), {
    c() {
      vt(t.$$.fragment);
    },
    m(a, r) {
      wt(t, a, r), e = !0;
    },
    p(a, r) {
      const i = r & /*gradio, loading_status*/
      6 ? Cn(n, [
        r & /*gradio*/
        4 && { autoscroll: (
          /*gradio*/
          a[2].autoscroll
        ) },
        r & /*gradio*/
        4 && { i18n: (
          /*gradio*/
          a[2].i18n
        ) },
        r & /*loading_status*/
        2 && qn(
          /*loading_status*/
          a[1]
        )
      ]) : {};
      t.$set(i);
    },
    i(a) {
      e || (fe(t.$$.fragment, a), e = !0);
    },
    o(a) {
      we(t.$$.fragment, a), e = !1;
    },
    d(a) {
      yt(t, a);
    }
  };
}
function Pn(l) {
  let t, e, n, s = (
    /*loading_status*/
    l[1] && ot(l)
  );
  return e = new jt({
    props: {
      docs: (
        /*value*/
        l[0]
      ),
      linkify: (
        /*linkify*/
        l[3]
      )
    }
  }), {
    c() {
      s && s.c(), t = Mn(), vt(e.$$.fragment);
    },
    m(a, r) {
      s && s.m(a, r), xn(a, t, r), wt(e, a, r), n = !0;
    },
    p(a, [r]) {
      /*loading_status*/
      a[1] ? s ? (s.p(a, r), r & /*loading_status*/
      2 && fe(s, 1)) : (s = ot(a), s.c(), fe(s, 1), s.m(t.parentNode, t)) : s && (Ln(), we(s, 1, 1, () => {
        s = null;
      }), Sn());
      const i = {};
      r & /*value*/
      1 && (i.docs = /*value*/
      a[0]), r & /*linkify*/
      8 && (i.linkify = /*linkify*/
      a[3]), e.$set(i);
    },
    i(a) {
      n || (fe(s), fe(e.$$.fragment, a), n = !0);
    },
    o(a) {
      we(s), we(e.$$.fragment, a), n = !1;
    },
    d(a) {
      a && En(t), s && s.d(a), yt(e, a);
    }
  };
}
function jn(l, t, e) {
  let { elem_id: n = "" } = t, { elem_classes: s = [] } = t, { visible: a = !0 } = t, { value: r } = t, { container: i = !0 } = t, { scale: u = null } = t, { min_width: f = void 0 } = t, { loading_status: _ } = t, { gradio: y } = t, { linkify: F = [] } = t;
  return l.$$set = (m) => {
    "elem_id" in m && e(4, n = m.elem_id), "elem_classes" in m && e(5, s = m.elem_classes), "visible" in m && e(6, a = m.visible), "value" in m && e(0, r = m.value), "container" in m && e(7, i = m.container), "scale" in m && e(8, u = m.scale), "min_width" in m && e(9, f = m.min_width), "loading_status" in m && e(1, _ = m.loading_status), "gradio" in m && e(2, y = m.gradio), "linkify" in m && e(3, F = m.linkify);
  }, [
    r,
    _,
    y,
    F,
    n,
    s,
    a,
    i,
    u,
    f
  ];
}
class Dn extends Fn {
  constructor(t) {
    super(), Tn(this, t, jn, Pn, zn, {
      elem_id: 4,
      elem_classes: 5,
      visible: 6,
      value: 0,
      container: 7,
      scale: 8,
      min_width: 9,
      loading_status: 1,
      gradio: 2,
      linkify: 3
    });
  }
}
export {
  Dn as default
};

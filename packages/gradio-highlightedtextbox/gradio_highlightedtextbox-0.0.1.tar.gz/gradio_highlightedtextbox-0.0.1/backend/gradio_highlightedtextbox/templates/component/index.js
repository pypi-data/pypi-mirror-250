const {
  SvelteComponent: el,
  assign: tl,
  create_slot: ll,
  detach: nl,
  element: il,
  get_all_dirty_from_scope: sl,
  get_slot_changes: ol,
  get_spread_update: fl,
  init: _l,
  insert: al,
  safe_not_equal: rl,
  set_dynamic_element_data: et,
  set_style: N,
  toggle_class: x,
  transition_in: Ot,
  transition_out: Rt,
  update_slot_base: ul
} = window.__gradio__svelte__internal;
function cl(n) {
  let e, t, l;
  const i = (
    /*#slots*/
    n[18].default
  ), s = ll(
    i,
    n,
    /*$$scope*/
    n[17],
    null
  );
  let o = [
    { "data-testid": (
      /*test_id*/
      n[7]
    ) },
    { id: (
      /*elem_id*/
      n[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      n[3].join(" ") + " svelte-1t38q2d"
    }
  ], _ = {};
  for (let f = 0; f < o.length; f += 1)
    _ = tl(_, o[f]);
  return {
    c() {
      e = il(
        /*tag*/
        n[14]
      ), s && s.c(), et(
        /*tag*/
        n[14]
      )(e, _), x(
        e,
        "hidden",
        /*visible*/
        n[10] === !1
      ), x(
        e,
        "padded",
        /*padding*/
        n[6]
      ), x(
        e,
        "border_focus",
        /*border_mode*/
        n[5] === "focus"
      ), x(e, "hide-container", !/*explicit_call*/
      n[8] && !/*container*/
      n[9]), N(
        e,
        "height",
        /*get_dimension*/
        n[15](
          /*height*/
          n[0]
        )
      ), N(e, "width", typeof /*width*/
      n[1] == "number" ? `calc(min(${/*width*/
      n[1]}px, 100%))` : (
        /*get_dimension*/
        n[15](
          /*width*/
          n[1]
        )
      )), N(
        e,
        "border-style",
        /*variant*/
        n[4]
      ), N(
        e,
        "overflow",
        /*allow_overflow*/
        n[11] ? "visible" : "hidden"
      ), N(
        e,
        "flex-grow",
        /*scale*/
        n[12]
      ), N(e, "min-width", `calc(min(${/*min_width*/
      n[13]}px, 100%))`), N(e, "border-width", "var(--block-border-width)");
    },
    m(f, a) {
      al(f, e, a), s && s.m(e, null), l = !0;
    },
    p(f, a) {
      s && s.p && (!l || a & /*$$scope*/
      131072) && ul(
        s,
        i,
        f,
        /*$$scope*/
        f[17],
        l ? ol(
          i,
          /*$$scope*/
          f[17],
          a,
          null
        ) : sl(
          /*$$scope*/
          f[17]
        ),
        null
      ), et(
        /*tag*/
        f[14]
      )(e, _ = fl(o, [
        (!l || a & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          f[7]
        ) },
        (!l || a & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          f[2]
        ) },
        (!l || a & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        f[3].join(" ") + " svelte-1t38q2d")) && { class: t }
      ])), x(
        e,
        "hidden",
        /*visible*/
        f[10] === !1
      ), x(
        e,
        "padded",
        /*padding*/
        f[6]
      ), x(
        e,
        "border_focus",
        /*border_mode*/
        f[5] === "focus"
      ), x(e, "hide-container", !/*explicit_call*/
      f[8] && !/*container*/
      f[9]), a & /*height*/
      1 && N(
        e,
        "height",
        /*get_dimension*/
        f[15](
          /*height*/
          f[0]
        )
      ), a & /*width*/
      2 && N(e, "width", typeof /*width*/
      f[1] == "number" ? `calc(min(${/*width*/
      f[1]}px, 100%))` : (
        /*get_dimension*/
        f[15](
          /*width*/
          f[1]
        )
      )), a & /*variant*/
      16 && N(
        e,
        "border-style",
        /*variant*/
        f[4]
      ), a & /*allow_overflow*/
      2048 && N(
        e,
        "overflow",
        /*allow_overflow*/
        f[11] ? "visible" : "hidden"
      ), a & /*scale*/
      4096 && N(
        e,
        "flex-grow",
        /*scale*/
        f[12]
      ), a & /*min_width*/
      8192 && N(e, "min-width", `calc(min(${/*min_width*/
      f[13]}px, 100%))`);
    },
    i(f) {
      l || (Ot(s, f), l = !0);
    },
    o(f) {
      Rt(s, f), l = !1;
    },
    d(f) {
      f && nl(e), s && s.d(f);
    }
  };
}
function dl(n) {
  let e, t = (
    /*tag*/
    n[14] && cl(n)
  );
  return {
    c() {
      t && t.c();
    },
    m(l, i) {
      t && t.m(l, i), e = !0;
    },
    p(l, [i]) {
      /*tag*/
      l[14] && t.p(l, i);
    },
    i(l) {
      e || (Ot(t, l), e = !0);
    },
    o(l) {
      Rt(t, l), e = !1;
    },
    d(l) {
      t && t.d(l);
    }
  };
}
function ml(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { height: s = void 0 } = e, { width: o = void 0 } = e, { elem_id: _ = "" } = e, { elem_classes: f = [] } = e, { variant: a = "solid" } = e, { border_mode: r = "base" } = e, { padding: u = !0 } = e, { type: c = "normal" } = e, { test_id: m = void 0 } = e, { explicit_call: p = !1 } = e, { container: T = !0 } = e, { visible: L = !0 } = e, { allow_overflow: S = !0 } = e, { scale: C = null } = e, { min_width: d = 0 } = e, y = c === "fieldset" ? "fieldset" : "div";
  const M = (h) => {
    if (h !== void 0) {
      if (typeof h == "number")
        return h + "px";
      if (typeof h == "string")
        return h;
    }
  };
  return n.$$set = (h) => {
    "height" in h && t(0, s = h.height), "width" in h && t(1, o = h.width), "elem_id" in h && t(2, _ = h.elem_id), "elem_classes" in h && t(3, f = h.elem_classes), "variant" in h && t(4, a = h.variant), "border_mode" in h && t(5, r = h.border_mode), "padding" in h && t(6, u = h.padding), "type" in h && t(16, c = h.type), "test_id" in h && t(7, m = h.test_id), "explicit_call" in h && t(8, p = h.explicit_call), "container" in h && t(9, T = h.container), "visible" in h && t(10, L = h.visible), "allow_overflow" in h && t(11, S = h.allow_overflow), "scale" in h && t(12, C = h.scale), "min_width" in h && t(13, d = h.min_width), "$$scope" in h && t(17, i = h.$$scope);
  }, [
    s,
    o,
    _,
    f,
    a,
    r,
    u,
    m,
    p,
    T,
    L,
    S,
    C,
    d,
    y,
    M,
    c,
    i,
    l
  ];
}
class bl extends el {
  constructor(e) {
    super(), _l(this, e, ml, dl, rl, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: hl,
  attr: gl,
  create_slot: wl,
  detach: pl,
  element: kl,
  get_all_dirty_from_scope: vl,
  get_slot_changes: yl,
  init: Cl,
  insert: ql,
  safe_not_equal: Ll,
  transition_in: Sl,
  transition_out: Tl,
  update_slot_base: Fl
} = window.__gradio__svelte__internal;
function Ml(n) {
  let e, t;
  const l = (
    /*#slots*/
    n[1].default
  ), i = wl(
    l,
    n,
    /*$$scope*/
    n[0],
    null
  );
  return {
    c() {
      e = kl("div"), i && i.c(), gl(e, "class", "svelte-1hnfib2");
    },
    m(s, o) {
      ql(s, e, o), i && i.m(e, null), t = !0;
    },
    p(s, [o]) {
      i && i.p && (!t || o & /*$$scope*/
      1) && Fl(
        i,
        l,
        s,
        /*$$scope*/
        s[0],
        t ? yl(
          l,
          /*$$scope*/
          s[0],
          o,
          null
        ) : vl(
          /*$$scope*/
          s[0]
        ),
        null
      );
    },
    i(s) {
      t || (Sl(i, s), t = !0);
    },
    o(s) {
      Tl(i, s), t = !1;
    },
    d(s) {
      s && pl(e), i && i.d(s);
    }
  };
}
function jl(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e;
  return n.$$set = (s) => {
    "$$scope" in s && t(0, i = s.$$scope);
  }, [i, l];
}
class Vl extends hl {
  constructor(e) {
    super(), Cl(this, e, jl, Ml, Ll, {});
  }
}
const {
  SvelteComponent: Hl,
  attr: tt,
  check_outros: Nl,
  create_component: zl,
  create_slot: Zl,
  destroy_component: Al,
  detach: je,
  element: Bl,
  empty: Pl,
  get_all_dirty_from_scope: Dl,
  get_slot_changes: El,
  group_outros: Il,
  init: Ol,
  insert: Ve,
  mount_component: Rl,
  safe_not_equal: Ul,
  set_data: Xl,
  space: Yl,
  text: Gl,
  toggle_class: ue,
  transition_in: ve,
  transition_out: He,
  update_slot_base: Wl
} = window.__gradio__svelte__internal;
function lt(n) {
  let e, t;
  return e = new Vl({
    props: {
      $$slots: { default: [Jl] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      zl(e.$$.fragment);
    },
    m(l, i) {
      Rl(e, l, i), t = !0;
    },
    p(l, i) {
      const s = {};
      i & /*$$scope, info*/
      10 && (s.$$scope = { dirty: i, ctx: l }), e.$set(s);
    },
    i(l) {
      t || (ve(e.$$.fragment, l), t = !0);
    },
    o(l) {
      He(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Al(e, l);
    }
  };
}
function Jl(n) {
  let e;
  return {
    c() {
      e = Gl(
        /*info*/
        n[1]
      );
    },
    m(t, l) {
      Ve(t, e, l);
    },
    p(t, l) {
      l & /*info*/
      2 && Xl(
        e,
        /*info*/
        t[1]
      );
    },
    d(t) {
      t && je(e);
    }
  };
}
function Kl(n) {
  let e, t, l, i;
  const s = (
    /*#slots*/
    n[2].default
  ), o = Zl(
    s,
    n,
    /*$$scope*/
    n[3],
    null
  );
  let _ = (
    /*info*/
    n[1] && lt(n)
  );
  return {
    c() {
      e = Bl("span"), o && o.c(), t = Yl(), _ && _.c(), l = Pl(), tt(e, "data-testid", "block-info"), tt(e, "class", "svelte-22c38v"), ue(e, "sr-only", !/*show_label*/
      n[0]), ue(e, "hide", !/*show_label*/
      n[0]), ue(
        e,
        "has-info",
        /*info*/
        n[1] != null
      );
    },
    m(f, a) {
      Ve(f, e, a), o && o.m(e, null), Ve(f, t, a), _ && _.m(f, a), Ve(f, l, a), i = !0;
    },
    p(f, [a]) {
      o && o.p && (!i || a & /*$$scope*/
      8) && Wl(
        o,
        s,
        f,
        /*$$scope*/
        f[3],
        i ? El(
          s,
          /*$$scope*/
          f[3],
          a,
          null
        ) : Dl(
          /*$$scope*/
          f[3]
        ),
        null
      ), (!i || a & /*show_label*/
      1) && ue(e, "sr-only", !/*show_label*/
      f[0]), (!i || a & /*show_label*/
      1) && ue(e, "hide", !/*show_label*/
      f[0]), (!i || a & /*info*/
      2) && ue(
        e,
        "has-info",
        /*info*/
        f[1] != null
      ), /*info*/
      f[1] ? _ ? (_.p(f, a), a & /*info*/
      2 && ve(_, 1)) : (_ = lt(f), _.c(), ve(_, 1), _.m(l.parentNode, l)) : _ && (Il(), He(_, 1, 1, () => {
        _ = null;
      }), Nl());
    },
    i(f) {
      i || (ve(o, f), ve(_), i = !0);
    },
    o(f) {
      He(o, f), He(_), i = !1;
    },
    d(f) {
      f && (je(e), je(t), je(l)), o && o.d(f), _ && _.d(f);
    }
  };
}
function Ql(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { show_label: s = !0 } = e, { info: o = void 0 } = e;
  return n.$$set = (_) => {
    "show_label" in _ && t(0, s = _.show_label), "info" in _ && t(1, o = _.info), "$$scope" in _ && t(3, i = _.$$scope);
  }, [s, o, l, i];
}
class xl extends Hl {
  constructor(e) {
    super(), Ol(this, e, Ql, Kl, Ul, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: $l,
  append: en,
  attr: $,
  detach: tn,
  init: ln,
  insert: nn,
  noop: De,
  safe_not_equal: sn,
  svg_element: nt
} = window.__gradio__svelte__internal;
function on(n) {
  let e, t;
  return {
    c() {
      e = nt("svg"), t = nt("polyline"), $(t, "points", "20 6 9 17 4 12"), $(e, "xmlns", "http://www.w3.org/2000/svg"), $(e, "viewBox", "2 0 20 20"), $(e, "fill", "none"), $(e, "stroke", "currentColor"), $(e, "stroke-width", "3"), $(e, "stroke-linecap", "round"), $(e, "stroke-linejoin", "round");
    },
    m(l, i) {
      nn(l, e, i), en(e, t);
    },
    p: De,
    i: De,
    o: De,
    d(l) {
      l && tn(e);
    }
  };
}
class fn extends $l {
  constructor(e) {
    super(), ln(this, e, null, on, sn, {});
  }
}
const {
  SvelteComponent: _n,
  append: it,
  attr: ne,
  detach: an,
  init: rn,
  insert: un,
  noop: Ee,
  safe_not_equal: cn,
  svg_element: Ie
} = window.__gradio__svelte__internal;
function dn(n) {
  let e, t, l;
  return {
    c() {
      e = Ie("svg"), t = Ie("path"), l = Ie("path"), ne(t, "fill", "currentColor"), ne(t, "d", "M28 10v18H10V10h18m0-2H10a2 2 0 0 0-2 2v18a2 2 0 0 0 2 2h18a2 2 0 0 0 2-2V10a2 2 0 0 0-2-2Z"), ne(l, "fill", "currentColor"), ne(l, "d", "M4 18H2V4a2 2 0 0 1 2-2h14v2H4Z"), ne(e, "xmlns", "http://www.w3.org/2000/svg"), ne(e, "viewBox", "0 0 33 33"), ne(e, "color", "currentColor");
    },
    m(i, s) {
      un(i, e, s), it(e, t), it(e, l);
    },
    p: Ee,
    i: Ee,
    o: Ee,
    d(i) {
      i && an(e);
    }
  };
}
class mn extends _n {
  constructor(e) {
    super(), rn(this, e, null, dn, cn, {});
  }
}
const st = [
  "red",
  "green",
  "blue",
  "yellow",
  "purple",
  "teal",
  "orange",
  "cyan",
  "lime",
  "pink"
], bn = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], ot = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
}, ft = bn.reduce(
  (n, { color: e, primary: t, secondary: l }) => ({
    ...n,
    [e]: {
      primary: ot[e][t],
      secondary: ot[e][l]
    }
  }),
  {}
), hn = (n) => st[n % st.length];
function Ne() {
}
const gn = (n) => n;
function wn(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
const Ut = typeof window < "u";
let _t = Ut ? () => window.performance.now() : () => Date.now(), Xt = Ut ? (n) => requestAnimationFrame(n) : Ne;
const he = /* @__PURE__ */ new Set();
function Yt(n) {
  he.forEach((e) => {
    e.c(n) || (he.delete(e), e.f());
  }), he.size !== 0 && Xt(Yt);
}
function pn(n) {
  let e;
  return he.size === 0 && Xt(Yt), {
    promise: new Promise((t) => {
      he.add(e = { c: n, f: t });
    }),
    abort() {
      he.delete(e);
    }
  };
}
function kn(n, { delay: e = 0, duration: t = 400, easing: l = gn } = {}) {
  const i = +getComputedStyle(n).opacity;
  return {
    delay: e,
    duration: t,
    easing: l,
    css: (s) => `opacity: ${s * i}`
  };
}
const ce = [];
function vn(n, e = Ne) {
  let t;
  const l = /* @__PURE__ */ new Set();
  function i(_) {
    if (wn(n, _) && (n = _, t)) {
      const f = !ce.length;
      for (const a of l)
        a[1](), ce.push(a, n);
      if (f) {
        for (let a = 0; a < ce.length; a += 2)
          ce[a][0](ce[a + 1]);
        ce.length = 0;
      }
    }
  }
  function s(_) {
    i(_(n));
  }
  function o(_, f = Ne) {
    const a = [_, f];
    return l.add(a), l.size === 1 && (t = e(i, s) || Ne), _(n), () => {
      l.delete(a), l.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: s, subscribe: o };
}
function at(n) {
  return Object.prototype.toString.call(n) === "[object Date]";
}
function Re(n, e, t, l) {
  if (typeof t == "number" || at(t)) {
    const i = l - t, s = (t - e) / (n.dt || 1 / 60), o = n.opts.stiffness * i, _ = n.opts.damping * s, f = (o - _) * n.inv_mass, a = (s + f) * n.dt;
    return Math.abs(a) < n.opts.precision && Math.abs(i) < n.opts.precision ? l : (n.settled = !1, at(t) ? new Date(t.getTime() + a) : t + a);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, s) => Re(n, e[s], t[s], l[s])
      );
    if (typeof t == "object") {
      const i = {};
      for (const s in t)
        i[s] = Re(n, e[s], t[s], l[s]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function rt(n, e = {}) {
  const t = vn(n), { stiffness: l = 0.15, damping: i = 0.8, precision: s = 0.01 } = e;
  let o, _, f, a = n, r = n, u = 1, c = 0, m = !1;
  function p(L, S = {}) {
    r = L;
    const C = f = {};
    return n == null || S.hard || T.stiffness >= 1 && T.damping >= 1 ? (m = !0, o = _t(), a = L, t.set(n = r), Promise.resolve()) : (S.soft && (c = 1 / ((S.soft === !0 ? 0.5 : +S.soft) * 60), u = 0), _ || (o = _t(), m = !1, _ = pn((d) => {
      if (m)
        return m = !1, _ = null, !1;
      u = Math.min(u + c, 1);
      const y = {
        inv_mass: u,
        opts: T,
        settled: !0,
        dt: (d - o) * 60 / 1e3
      }, M = Re(y, a, n, r);
      return o = d, a = n, t.set(n = M), y.settled && (_ = null), !y.settled;
    })), new Promise((d) => {
      _.promise.then(() => {
        C === f && d();
      });
    }));
  }
  const T = {
    set: p,
    update: (L, S) => p(L(r, n), S),
    subscribe: t.subscribe,
    stiffness: l,
    damping: i,
    precision: s
  };
  return T;
}
function ut(n, e, t) {
  if (!t) {
    var l = document.createElement("canvas");
    t = l.getContext("2d");
  }
  t.fillStyle = n, t.fillRect(0, 0, 1, 1);
  const [i, s, o] = t.getImageData(0, 0, 1, 1).data;
  return t.clearRect(0, 0, 1, 1), `rgba(${i}, ${s}, ${o}, ${255 / e})`;
}
function yn(n, e, t) {
  var l = {};
  for (const i in n) {
    const s = n[i].trim();
    s in ft ? l[i] = ft[s] : l[i] = {
      primary: e ? ut(n[i], 1, t) : n[i],
      secondary: e ? ut(n[i], 0.5, t) : n[i]
    };
  }
  return l;
}
function Cn(n, e) {
  let t = [], l = null, i = null;
  for (const [s, o] of n)
    e === "empty" && o === null || e === "equal" && i === o ? l = l ? l + s : s : (l !== null && t.push([l, i]), l = s, i = o);
  return l !== null && t.push([l, i]), t;
}
const {
  SvelteComponent: qn,
  add_render_callback: Xe,
  append: se,
  attr: V,
  binding_callbacks: ct,
  bubble: de,
  check_outros: Gt,
  create_component: Ye,
  create_in_transition: Ln,
  destroy_component: Ge,
  destroy_each: Sn,
  detach: G,
  element: le,
  empty: Tn,
  ensure_array_like: dt,
  group_outros: Wt,
  init: Fn,
  insert: W,
  listen: U,
  mount_component: We,
  noop: Jt,
  run_all: Mn,
  safe_not_equal: jn,
  set_data: Je,
  space: ye,
  text: Ke,
  toggle_class: mt,
  transition_in: ee,
  transition_out: oe
} = window.__gradio__svelte__internal, { beforeUpdate: Vn, afterUpdate: Hn, createEventDispatcher: Nn, tick: Ei } = window.__gradio__svelte__internal;
function bt(n, e, t) {
  const l = n.slice();
  return l[39] = e[t][0], l[40] = e[t][1], l[42] = t, l;
}
function ht(n) {
  let e, t, l = (
    /*show_legend_label*/
    n[5] && gt(n)
  ), i = dt(Object.entries(
    /*_color_map*/
    n[12]
  )), s = [];
  for (let o = 0; o < i.length; o += 1)
    s[o] = wt(bt(n, i, o));
  return {
    c() {
      e = le("div"), l && l.c(), t = ye();
      for (let o = 0; o < s.length; o += 1)
        s[o].c();
      V(e, "class", "category-legend svelte-1t4levu"), V(e, "data-testid", "highlighted-text:category-legend");
    },
    m(o, _) {
      W(o, e, _), l && l.m(e, null), se(e, t);
      for (let f = 0; f < s.length; f += 1)
        s[f] && s[f].m(e, null);
    },
    p(o, _) {
      if (/*show_legend_label*/
      o[5] ? l ? l.p(o, _) : (l = gt(o), l.c(), l.m(e, t)) : l && (l.d(1), l = null), _[0] & /*_color_map*/
      4096) {
        i = dt(Object.entries(
          /*_color_map*/
          o[12]
        ));
        let f;
        for (f = 0; f < i.length; f += 1) {
          const a = bt(o, i, f);
          s[f] ? s[f].p(a, _) : (s[f] = wt(a), s[f].c(), s[f].m(e, null));
        }
        for (; f < s.length; f += 1)
          s[f].d(1);
        s.length = i.length;
      }
    },
    d(o) {
      o && G(e), l && l.d(), Sn(s, o);
    }
  };
}
function gt(n) {
  let e, t;
  return {
    c() {
      e = le("div"), t = Ke(
        /*legend_label*/
        n[1]
      ), V(e, "class", "legend-description svelte-1t4levu");
    },
    m(l, i) {
      W(l, e, i), se(e, t);
    },
    p(l, i) {
      i[0] & /*legend_label*/
      2 && Je(
        t,
        /*legend_label*/
        l[1]
      );
    },
    d(l) {
      l && G(e);
    }
  };
}
function wt(n) {
  let e, t = (
    /*category*/
    n[39] + ""
  ), l, i, s;
  return {
    c() {
      e = le("div"), l = Ke(t), i = ye(), V(e, "class", "category-label svelte-1t4levu"), V(e, "style", s = "background-color:" + /*color*/
      n[40].secondary);
    },
    m(o, _) {
      W(o, e, _), se(e, l), se(e, i);
    },
    p(o, _) {
      _[0] & /*_color_map*/
      4096 && t !== (t = /*category*/
      o[39] + "") && Je(l, t), _[0] & /*_color_map*/
      4096 && s !== (s = "background-color:" + /*color*/
      o[40].secondary) && V(e, "style", s);
    },
    d(o) {
      o && G(e);
    }
  };
}
function zn(n) {
  let e;
  return {
    c() {
      e = Ke(
        /*label*/
        n[0]
      );
    },
    m(t, l) {
      W(t, e, l);
    },
    p(t, l) {
      l[0] & /*label*/
      1 && Je(
        e,
        /*label*/
        t[0]
      );
    },
    d(t) {
      t && G(e);
    }
  };
}
function pt(n) {
  let e, t, l, i;
  const s = [An, Zn], o = [];
  function _(f, a) {
    return (
      /*copied*/
      f[13] ? 0 : 1
    );
  }
  return e = _(n), t = o[e] = s[e](n), {
    c() {
      t.c(), l = Tn();
    },
    m(f, a) {
      o[e].m(f, a), W(f, l, a), i = !0;
    },
    p(f, a) {
      let r = e;
      e = _(f), e === r ? o[e].p(f, a) : (Wt(), oe(o[r], 1, 1, () => {
        o[r] = null;
      }), Gt(), t = o[e], t ? t.p(f, a) : (t = o[e] = s[e](f), t.c()), ee(t, 1), t.m(l.parentNode, l));
    },
    i(f) {
      i || (ee(t), i = !0);
    },
    o(f) {
      oe(t), i = !1;
    },
    d(f) {
      f && G(l), o[e].d(f);
    }
  };
}
function Zn(n) {
  let e, t, l, i, s;
  return t = new mn({}), {
    c() {
      e = le("button"), Ye(t.$$.fragment), V(e, "aria-label", "Copy"), V(e, "aria-roledescription", "Copy text"), V(e, "class", "svelte-1t4levu");
    },
    m(o, _) {
      W(o, e, _), We(t, e, null), l = !0, i || (s = U(
        e,
        "click",
        /*handle_copy*/
        n[15]
      ), i = !0);
    },
    p: Jt,
    i(o) {
      l || (ee(t.$$.fragment, o), l = !0);
    },
    o(o) {
      oe(t.$$.fragment, o), l = !1;
    },
    d(o) {
      o && G(e), Ge(t), i = !1, s();
    }
  };
}
function An(n) {
  let e, t, l, i;
  return t = new fn({}), {
    c() {
      e = le("button"), Ye(t.$$.fragment), V(e, "aria-label", "Copied"), V(e, "aria-roledescription", "Text copied"), V(e, "class", "svelte-1t4levu");
    },
    m(s, o) {
      W(s, e, o), We(t, e, null), i = !0;
    },
    p: Jt,
    i(s) {
      i || (ee(t.$$.fragment, s), s && (l || Xe(() => {
        l = Ln(e, kn, { duration: 300 }), l.start();
      })), i = !0);
    },
    o(s) {
      oe(t.$$.fragment, s), i = !1;
    },
    d(s) {
      s && G(e), Ge(t);
    }
  };
}
function Bn(n) {
  let e, t, l;
  return {
    c() {
      e = le("div"), V(e, "class", "textfield svelte-1t4levu"), V(e, "data-testid", "highlighted-textbox"), V(e, "contenteditable", "true"), /*el_text*/
      (n[11] === void 0 || /*marked_el_text*/
      n[9] === void 0) && Xe(() => (
        /*div_input_handler_1*/
        n[28].call(e)
      ));
    },
    m(i, s) {
      W(i, e, s), n[27](e), /*el_text*/
      n[11] !== void 0 && (e.textContent = /*el_text*/
      n[11]), /*marked_el_text*/
      n[9] !== void 0 && (e.innerHTML = /*marked_el_text*/
      n[9]), t || (l = [
        U(
          e,
          "input",
          /*div_input_handler_1*/
          n[28]
        ),
        U(
          e,
          "blur",
          /*handle_blur*/
          n[14]
        ),
        U(
          e,
          "keypress",
          /*keypress_handler*/
          n[19]
        ),
        U(
          e,
          "select",
          /*select_handler*/
          n[20]
        ),
        U(
          e,
          "scroll",
          /*scroll_handler*/
          n[21]
        ),
        U(
          e,
          "input",
          /*input_handler*/
          n[22]
        ),
        U(
          e,
          "focus",
          /*focus_handler*/
          n[23]
        ),
        U(
          e,
          "change",
          /*change_handler*/
          n[24]
        )
      ], t = !0);
    },
    p(i, s) {
      s[0] & /*el_text*/
      2048 && /*el_text*/
      i[11] !== e.textContent && (e.textContent = /*el_text*/
      i[11]), s[0] & /*marked_el_text*/
      512 && /*marked_el_text*/
      i[9] !== e.innerHTML && (e.innerHTML = /*marked_el_text*/
      i[9]);
    },
    d(i) {
      i && G(e), n[27](null), t = !1, Mn(l);
    }
  };
}
function Pn(n) {
  let e, t, l;
  return {
    c() {
      e = le("div"), V(e, "class", "textfield svelte-1t4levu"), V(e, "data-testid", "highlighted-textbox"), V(e, "contenteditable", "false"), /*el_text*/
      (n[11] === void 0 || /*marked_el_text*/
      n[9] === void 0) && Xe(() => (
        /*div_input_handler*/
        n[26].call(e)
      ));
    },
    m(i, s) {
      W(i, e, s), n[25](e), /*el_text*/
      n[11] !== void 0 && (e.textContent = /*el_text*/
      n[11]), /*marked_el_text*/
      n[9] !== void 0 && (e.innerHTML = /*marked_el_text*/
      n[9]), t || (l = U(
        e,
        "input",
        /*div_input_handler*/
        n[26]
      ), t = !0);
    },
    p(i, s) {
      s[0] & /*el_text*/
      2048 && /*el_text*/
      i[11] !== e.textContent && (e.textContent = /*el_text*/
      i[11]), s[0] & /*marked_el_text*/
      512 && /*marked_el_text*/
      i[9] !== e.innerHTML && (e.innerHTML = /*marked_el_text*/
      i[9]);
    },
    d(i) {
      i && G(e), n[25](null), t = !1, l();
    }
  };
}
function Dn(n) {
  let e, t, l, i, s, o, _ = (
    /*show_legend*/
    n[4] && ht(n)
  );
  l = new xl({
    props: {
      show_label: (
        /*show_label*/
        n[3]
      ),
      info: (
        /*info*/
        n[2]
      ),
      $$slots: { default: [zn] },
      $$scope: { ctx: n }
    }
  });
  let f = (
    /*show_copy_button*/
    n[7] && pt(n)
  );
  function a(c, m) {
    return (
      /*disabled*/
      c[8] ? Pn : Bn
    );
  }
  let r = a(n), u = r(n);
  return {
    c() {
      e = le("label"), _ && _.c(), t = ye(), Ye(l.$$.fragment), i = ye(), f && f.c(), s = ye(), u.c(), V(e, "class", "svelte-1t4levu"), mt(
        e,
        "container",
        /*container*/
        n[6]
      );
    },
    m(c, m) {
      W(c, e, m), _ && _.m(e, null), se(e, t), We(l, e, null), se(e, i), f && f.m(e, null), se(e, s), u.m(e, null), o = !0;
    },
    p(c, m) {
      /*show_legend*/
      c[4] ? _ ? _.p(c, m) : (_ = ht(c), _.c(), _.m(e, t)) : _ && (_.d(1), _ = null);
      const p = {};
      m[0] & /*show_label*/
      8 && (p.show_label = /*show_label*/
      c[3]), m[0] & /*info*/
      4 && (p.info = /*info*/
      c[2]), m[0] & /*label*/
      1 | m[1] & /*$$scope*/
      4096 && (p.$$scope = { dirty: m, ctx: c }), l.$set(p), /*show_copy_button*/
      c[7] ? f ? (f.p(c, m), m[0] & /*show_copy_button*/
      128 && ee(f, 1)) : (f = pt(c), f.c(), ee(f, 1), f.m(e, s)) : f && (Wt(), oe(f, 1, 1, () => {
        f = null;
      }), Gt()), r === (r = a(c)) && u ? u.p(c, m) : (u.d(1), u = r(c), u && (u.c(), u.m(e, null))), (!o || m[0] & /*container*/
      64) && mt(
        e,
        "container",
        /*container*/
        c[6]
      );
    },
    i(c) {
      o || (ee(l.$$.fragment, c), ee(f), o = !0);
    },
    o(c) {
      oe(l.$$.fragment, c), oe(f), o = !1;
    },
    d(c) {
      c && G(e), _ && _.d(), Ge(l), f && f.d(), u.d();
    }
  };
}
function En(n) {
  let e, t = n[0], l = 1;
  for (; l < n.length; ) {
    const i = n[l], s = n[l + 1];
    if (l += 2, (i === "optionalAccess" || i === "optionalCall") && t == null)
      return;
    i === "access" || i === "optionalAccess" ? (e = t, t = s(t)) : (i === "call" || i === "optionalCall") && (t = s((...o) => t.call(e, ...o)), e = void 0);
  }
  return t;
}
function In(n, e, t) {
  const l = typeof document < "u";
  let { value: i = [] } = e, { value_is_output: s = !1 } = e, { label: o } = e, { legend_label: _ } = e, { info: f = void 0 } = e, { show_label: a = !0 } = e, { show_legend: r = !1 } = e, { show_legend_label: u = !1 } = e, { container: c = !0 } = e, { color_map: m = {} } = e, { show_copy_button: p = !1 } = e, { disabled: T } = e, L, S = "", C = "", d, y = {}, M = {}, h = !1, P;
  function J() {
    if (!m || Object.keys(m).length === 0 ? y = {} : y = m, i.length > 0) {
      for (let [b, H] of i)
        if (H !== null && !(H in y)) {
          let re = hn(Object.keys(y).length);
          y[H] = re;
        }
    }
    t(12, M = yn(y, l, d));
  }
  function z() {
    i.length > 0 && s && (t(11, S = i.map(([b, H]) => b).join(" ")), t(9, C = i.map(([b, H]) => H !== null ? `<mark class="hl ${H}" style="background-color:${M[H].secondary}">${b}</mark>` : b).join(" ") + " "));
  }
  const D = Nn();
  Vn(() => {
    L && L.offsetHeight + L.scrollTop > L.scrollHeight - 100;
  });
  function R() {
    D("change", C), s || D("input");
  }
  Hn(() => {
    J(), z(), t(17, s = !1);
  });
  function fe() {
    let b = [], H = "", re = null, Be = !1, Se = "";
    for (let Pe = 0; Pe < C.length; Pe++) {
      let Te = C[Pe];
      Te === "<" ? (Be = !0, H && b.push([H, re]), H = "", re = null) : Te === ">" ? (Be = !1, Se.startsWith("mark") && (re = En([
        Se,
        "access",
        (ke) => ke.match,
        "call",
        (ke) => ke(/class="hl ([^"]+)"/),
        "optionalAccess",
        (ke) => ke[1]
      ]) || null), Se = "") : Be ? Se += Te : H += Te;
    }
    H && b.push([H, re]), t(16, i = b);
  }
  async function E() {
    "clipboard" in navigator && (await navigator.clipboard.writeText(S), K());
  }
  function K() {
    t(13, h = !0), P && clearTimeout(P), P = setTimeout(
      () => {
        t(13, h = !1);
      },
      1e3
    );
  }
  function Z(b) {
    de.call(this, n, b);
  }
  function _e(b) {
    de.call(this, n, b);
  }
  function g(b) {
    de.call(this, n, b);
  }
  function qe(b) {
    de.call(this, n, b);
  }
  function Le(b) {
    de.call(this, n, b);
  }
  function ae(b) {
    de.call(this, n, b);
  }
  function Ze(b) {
    ct[b ? "unshift" : "push"](() => {
      L = b, t(10, L);
    });
  }
  function Ae() {
    S = this.textContent, C = this.innerHTML, t(11, S), t(9, C);
  }
  function w(b) {
    ct[b ? "unshift" : "push"](() => {
      L = b, t(10, L);
    });
  }
  function $t() {
    S = this.textContent, C = this.innerHTML, t(11, S), t(9, C);
  }
  return n.$$set = (b) => {
    "value" in b && t(16, i = b.value), "value_is_output" in b && t(17, s = b.value_is_output), "label" in b && t(0, o = b.label), "legend_label" in b && t(1, _ = b.legend_label), "info" in b && t(2, f = b.info), "show_label" in b && t(3, a = b.show_label), "show_legend" in b && t(4, r = b.show_legend), "show_legend_label" in b && t(5, u = b.show_legend_label), "container" in b && t(6, c = b.container), "color_map" in b && t(18, m = b.color_map), "show_copy_button" in b && t(7, p = b.show_copy_button), "disabled" in b && t(8, T = b.disabled);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*marked_el_text*/
    512 && R();
  }, z(), J(), [
    o,
    _,
    f,
    a,
    r,
    u,
    c,
    p,
    T,
    C,
    L,
    S,
    M,
    h,
    fe,
    E,
    i,
    s,
    m,
    Z,
    _e,
    g,
    qe,
    Le,
    ae,
    Ze,
    Ae,
    w,
    $t
  ];
}
class On extends qn {
  constructor(e) {
    super(), Fn(
      this,
      e,
      In,
      Dn,
      jn,
      {
        value: 16,
        value_is_output: 17,
        label: 0,
        legend_label: 1,
        info: 2,
        show_label: 3,
        show_legend: 4,
        show_legend_label: 5,
        container: 6,
        color_map: 18,
        show_copy_button: 7,
        disabled: 8
      },
      null,
      [-1, -1]
    );
  }
}
function me(n) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; n > 1e3 && t < e.length - 1; )
    n /= 1e3, t++;
  let l = e[t];
  return (Number.isInteger(n) ? n : n.toFixed(1)) + l;
}
const {
  SvelteComponent: Rn,
  append: I,
  attr: q,
  component_subscribe: kt,
  detach: Un,
  element: Xn,
  init: Yn,
  insert: Gn,
  noop: vt,
  safe_not_equal: Wn,
  set_style: Fe,
  svg_element: O,
  toggle_class: yt
} = window.__gradio__svelte__internal, { onMount: Jn } = window.__gradio__svelte__internal;
function Kn(n) {
  let e, t, l, i, s, o, _, f, a, r, u, c;
  return {
    c() {
      e = Xn("div"), t = O("svg"), l = O("g"), i = O("path"), s = O("path"), o = O("path"), _ = O("path"), f = O("g"), a = O("path"), r = O("path"), u = O("path"), c = O("path"), q(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), q(i, "fill", "#FF7C00"), q(i, "fill-opacity", "0.4"), q(i, "class", "svelte-43sxxs"), q(s, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), q(s, "fill", "#FF7C00"), q(s, "class", "svelte-43sxxs"), q(o, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), q(o, "fill", "#FF7C00"), q(o, "fill-opacity", "0.4"), q(o, "class", "svelte-43sxxs"), q(_, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), q(_, "fill", "#FF7C00"), q(_, "class", "svelte-43sxxs"), Fe(l, "transform", "translate(" + /*$top*/
      n[1][0] + "px, " + /*$top*/
      n[1][1] + "px)"), q(a, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), q(a, "fill", "#FF7C00"), q(a, "fill-opacity", "0.4"), q(a, "class", "svelte-43sxxs"), q(r, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), q(r, "fill", "#FF7C00"), q(r, "class", "svelte-43sxxs"), q(u, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), q(u, "fill", "#FF7C00"), q(u, "fill-opacity", "0.4"), q(u, "class", "svelte-43sxxs"), q(c, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), q(c, "fill", "#FF7C00"), q(c, "class", "svelte-43sxxs"), Fe(f, "transform", "translate(" + /*$bottom*/
      n[2][0] + "px, " + /*$bottom*/
      n[2][1] + "px)"), q(t, "viewBox", "-1200 -1200 3000 3000"), q(t, "fill", "none"), q(t, "xmlns", "http://www.w3.org/2000/svg"), q(t, "class", "svelte-43sxxs"), q(e, "class", "svelte-43sxxs"), yt(
        e,
        "margin",
        /*margin*/
        n[0]
      );
    },
    m(m, p) {
      Gn(m, e, p), I(e, t), I(t, l), I(l, i), I(l, s), I(l, o), I(l, _), I(t, f), I(f, a), I(f, r), I(f, u), I(f, c);
    },
    p(m, [p]) {
      p & /*$top*/
      2 && Fe(l, "transform", "translate(" + /*$top*/
      m[1][0] + "px, " + /*$top*/
      m[1][1] + "px)"), p & /*$bottom*/
      4 && Fe(f, "transform", "translate(" + /*$bottom*/
      m[2][0] + "px, " + /*$bottom*/
      m[2][1] + "px)"), p & /*margin*/
      1 && yt(
        e,
        "margin",
        /*margin*/
        m[0]
      );
    },
    i: vt,
    o: vt,
    d(m) {
      m && Un(e);
    }
  };
}
function Qn(n, e, t) {
  let l, i, { margin: s = !0 } = e;
  const o = rt([0, 0]);
  kt(n, o, (c) => t(1, l = c));
  const _ = rt([0, 0]);
  kt(n, _, (c) => t(2, i = c));
  let f;
  async function a() {
    await Promise.all([o.set([125, 140]), _.set([-125, -140])]), await Promise.all([o.set([-125, 140]), _.set([125, -140])]), await Promise.all([o.set([-125, 0]), _.set([125, -0])]), await Promise.all([o.set([125, 0]), _.set([-125, 0])]);
  }
  async function r() {
    await a(), f || r();
  }
  async function u() {
    await Promise.all([o.set([125, 0]), _.set([-125, 0])]), r();
  }
  return Jn(() => (u(), () => f = !0)), n.$$set = (c) => {
    "margin" in c && t(0, s = c.margin);
  }, [s, l, i, o, _];
}
class xn extends Rn {
  constructor(e) {
    super(), Yn(this, e, Qn, Kn, Wn, { margin: 0 });
  }
}
const {
  SvelteComponent: $n,
  append: ie,
  attr: X,
  binding_callbacks: Ct,
  check_outros: Kt,
  create_component: ei,
  create_slot: ti,
  destroy_component: li,
  destroy_each: Qt,
  detach: k,
  element: Q,
  empty: pe,
  ensure_array_like: ze,
  get_all_dirty_from_scope: ni,
  get_slot_changes: ii,
  group_outros: xt,
  init: si,
  insert: v,
  mount_component: oi,
  noop: Ue,
  safe_not_equal: fi,
  set_data: B,
  set_style: te,
  space: Y,
  text: F,
  toggle_class: A,
  transition_in: ge,
  transition_out: we,
  update_slot_base: _i
} = window.__gradio__svelte__internal, { tick: ai } = window.__gradio__svelte__internal, { onDestroy: ri } = window.__gradio__svelte__internal, ui = (n) => ({}), qt = (n) => ({});
function Lt(n, e, t) {
  const l = n.slice();
  return l[38] = e[t], l[40] = t, l;
}
function St(n, e, t) {
  const l = n.slice();
  return l[38] = e[t], l;
}
function ci(n) {
  let e, t = (
    /*i18n*/
    n[1]("common.error") + ""
  ), l, i, s;
  const o = (
    /*#slots*/
    n[29].error
  ), _ = ti(
    o,
    n,
    /*$$scope*/
    n[28],
    qt
  );
  return {
    c() {
      e = Q("span"), l = F(t), i = Y(), _ && _.c(), X(e, "class", "error svelte-1txqlrd");
    },
    m(f, a) {
      v(f, e, a), ie(e, l), v(f, i, a), _ && _.m(f, a), s = !0;
    },
    p(f, a) {
      (!s || a[0] & /*i18n*/
      2) && t !== (t = /*i18n*/
      f[1]("common.error") + "") && B(l, t), _ && _.p && (!s || a[0] & /*$$scope*/
      268435456) && _i(
        _,
        o,
        f,
        /*$$scope*/
        f[28],
        s ? ii(
          o,
          /*$$scope*/
          f[28],
          a,
          ui
        ) : ni(
          /*$$scope*/
          f[28]
        ),
        qt
      );
    },
    i(f) {
      s || (ge(_, f), s = !0);
    },
    o(f) {
      we(_, f), s = !1;
    },
    d(f) {
      f && (k(e), k(i)), _ && _.d(f);
    }
  };
}
function di(n) {
  let e, t, l, i, s, o, _, f, a, r = (
    /*variant*/
    n[8] === "default" && /*show_eta_bar*/
    n[18] && /*show_progress*/
    n[6] === "full" && Tt(n)
  );
  function u(d, y) {
    if (
      /*progress*/
      d[7]
    )
      return hi;
    if (
      /*queue_position*/
      d[2] !== null && /*queue_size*/
      d[3] !== void 0 && /*queue_position*/
      d[2] >= 0
    )
      return bi;
    if (
      /*queue_position*/
      d[2] === 0
    )
      return mi;
  }
  let c = u(n), m = c && c(n), p = (
    /*timer*/
    n[5] && jt(n)
  );
  const T = [ki, pi], L = [];
  function S(d, y) {
    return (
      /*last_progress_level*/
      d[15] != null ? 0 : (
        /*show_progress*/
        d[6] === "full" ? 1 : -1
      )
    );
  }
  ~(s = S(n)) && (o = L[s] = T[s](n));
  let C = !/*timer*/
  n[5] && Bt(n);
  return {
    c() {
      r && r.c(), e = Y(), t = Q("div"), m && m.c(), l = Y(), p && p.c(), i = Y(), o && o.c(), _ = Y(), C && C.c(), f = pe(), X(t, "class", "progress-text svelte-1txqlrd"), A(
        t,
        "meta-text-center",
        /*variant*/
        n[8] === "center"
      ), A(
        t,
        "meta-text",
        /*variant*/
        n[8] === "default"
      );
    },
    m(d, y) {
      r && r.m(d, y), v(d, e, y), v(d, t, y), m && m.m(t, null), ie(t, l), p && p.m(t, null), v(d, i, y), ~s && L[s].m(d, y), v(d, _, y), C && C.m(d, y), v(d, f, y), a = !0;
    },
    p(d, y) {
      /*variant*/
      d[8] === "default" && /*show_eta_bar*/
      d[18] && /*show_progress*/
      d[6] === "full" ? r ? r.p(d, y) : (r = Tt(d), r.c(), r.m(e.parentNode, e)) : r && (r.d(1), r = null), c === (c = u(d)) && m ? m.p(d, y) : (m && m.d(1), m = c && c(d), m && (m.c(), m.m(t, l))), /*timer*/
      d[5] ? p ? p.p(d, y) : (p = jt(d), p.c(), p.m(t, null)) : p && (p.d(1), p = null), (!a || y[0] & /*variant*/
      256) && A(
        t,
        "meta-text-center",
        /*variant*/
        d[8] === "center"
      ), (!a || y[0] & /*variant*/
      256) && A(
        t,
        "meta-text",
        /*variant*/
        d[8] === "default"
      );
      let M = s;
      s = S(d), s === M ? ~s && L[s].p(d, y) : (o && (xt(), we(L[M], 1, 1, () => {
        L[M] = null;
      }), Kt()), ~s ? (o = L[s], o ? o.p(d, y) : (o = L[s] = T[s](d), o.c()), ge(o, 1), o.m(_.parentNode, _)) : o = null), /*timer*/
      d[5] ? C && (C.d(1), C = null) : C ? C.p(d, y) : (C = Bt(d), C.c(), C.m(f.parentNode, f));
    },
    i(d) {
      a || (ge(o), a = !0);
    },
    o(d) {
      we(o), a = !1;
    },
    d(d) {
      d && (k(e), k(t), k(i), k(_), k(f)), r && r.d(d), m && m.d(), p && p.d(), ~s && L[s].d(d), C && C.d(d);
    }
  };
}
function Tt(n) {
  let e, t = `translateX(${/*eta_level*/
  (n[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = Q("div"), X(e, "class", "eta-bar svelte-1txqlrd"), te(e, "transform", t);
    },
    m(l, i) {
      v(l, e, i);
    },
    p(l, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (l[17] || 0) * 100 - 100}%)`) && te(e, "transform", t);
    },
    d(l) {
      l && k(e);
    }
  };
}
function mi(n) {
  let e;
  return {
    c() {
      e = F("processing |");
    },
    m(t, l) {
      v(t, e, l);
    },
    p: Ue,
    d(t) {
      t && k(e);
    }
  };
}
function bi(n) {
  let e, t = (
    /*queue_position*/
    n[2] + 1 + ""
  ), l, i, s, o;
  return {
    c() {
      e = F("queue: "), l = F(t), i = F("/"), s = F(
        /*queue_size*/
        n[3]
      ), o = F(" |");
    },
    m(_, f) {
      v(_, e, f), v(_, l, f), v(_, i, f), v(_, s, f), v(_, o, f);
    },
    p(_, f) {
      f[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      _[2] + 1 + "") && B(l, t), f[0] & /*queue_size*/
      8 && B(
        s,
        /*queue_size*/
        _[3]
      );
    },
    d(_) {
      _ && (k(e), k(l), k(i), k(s), k(o));
    }
  };
}
function hi(n) {
  let e, t = ze(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = Mt(St(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = pe();
    },
    m(i, s) {
      for (let o = 0; o < l.length; o += 1)
        l[o] && l[o].m(i, s);
      v(i, e, s);
    },
    p(i, s) {
      if (s[0] & /*progress*/
      128) {
        t = ze(
          /*progress*/
          i[7]
        );
        let o;
        for (o = 0; o < t.length; o += 1) {
          const _ = St(i, t, o);
          l[o] ? l[o].p(_, s) : (l[o] = Mt(_), l[o].c(), l[o].m(e.parentNode, e));
        }
        for (; o < l.length; o += 1)
          l[o].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && k(e), Qt(l, i);
    }
  };
}
function Ft(n) {
  let e, t = (
    /*p*/
    n[38].unit + ""
  ), l, i, s = " ", o;
  function _(r, u) {
    return (
      /*p*/
      r[38].length != null ? wi : gi
    );
  }
  let f = _(n), a = f(n);
  return {
    c() {
      a.c(), e = Y(), l = F(t), i = F(" | "), o = F(s);
    },
    m(r, u) {
      a.m(r, u), v(r, e, u), v(r, l, u), v(r, i, u), v(r, o, u);
    },
    p(r, u) {
      f === (f = _(r)) && a ? a.p(r, u) : (a.d(1), a = f(r), a && (a.c(), a.m(e.parentNode, e))), u[0] & /*progress*/
      128 && t !== (t = /*p*/
      r[38].unit + "") && B(l, t);
    },
    d(r) {
      r && (k(e), k(l), k(i), k(o)), a.d(r);
    }
  };
}
function gi(n) {
  let e = me(
    /*p*/
    n[38].index || 0
  ) + "", t;
  return {
    c() {
      t = F(e);
    },
    m(l, i) {
      v(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = me(
        /*p*/
        l[38].index || 0
      ) + "") && B(t, e);
    },
    d(l) {
      l && k(t);
    }
  };
}
function wi(n) {
  let e = me(
    /*p*/
    n[38].index || 0
  ) + "", t, l, i = me(
    /*p*/
    n[38].length
  ) + "", s;
  return {
    c() {
      t = F(e), l = F("/"), s = F(i);
    },
    m(o, _) {
      v(o, t, _), v(o, l, _), v(o, s, _);
    },
    p(o, _) {
      _[0] & /*progress*/
      128 && e !== (e = me(
        /*p*/
        o[38].index || 0
      ) + "") && B(t, e), _[0] & /*progress*/
      128 && i !== (i = me(
        /*p*/
        o[38].length
      ) + "") && B(s, i);
    },
    d(o) {
      o && (k(t), k(l), k(s));
    }
  };
}
function Mt(n) {
  let e, t = (
    /*p*/
    n[38].index != null && Ft(n)
  );
  return {
    c() {
      t && t.c(), e = pe();
    },
    m(l, i) {
      t && t.m(l, i), v(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[38].index != null ? t ? t.p(l, i) : (t = Ft(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && k(e), t && t.d(l);
    }
  };
}
function jt(n) {
  let e, t = (
    /*eta*/
    n[0] ? `/${/*formatted_eta*/
    n[19]}` : ""
  ), l, i;
  return {
    c() {
      e = F(
        /*formatted_timer*/
        n[20]
      ), l = F(t), i = F("s");
    },
    m(s, o) {
      v(s, e, o), v(s, l, o), v(s, i, o);
    },
    p(s, o) {
      o[0] & /*formatted_timer*/
      1048576 && B(
        e,
        /*formatted_timer*/
        s[20]
      ), o[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      s[0] ? `/${/*formatted_eta*/
      s[19]}` : "") && B(l, t);
    },
    d(s) {
      s && (k(e), k(l), k(i));
    }
  };
}
function pi(n) {
  let e, t;
  return e = new xn({
    props: { margin: (
      /*variant*/
      n[8] === "default"
    ) }
  }), {
    c() {
      ei(e.$$.fragment);
    },
    m(l, i) {
      oi(e, l, i), t = !0;
    },
    p(l, i) {
      const s = {};
      i[0] & /*variant*/
      256 && (s.margin = /*variant*/
      l[8] === "default"), e.$set(s);
    },
    i(l) {
      t || (ge(e.$$.fragment, l), t = !0);
    },
    o(l) {
      we(e.$$.fragment, l), t = !1;
    },
    d(l) {
      li(e, l);
    }
  };
}
function ki(n) {
  let e, t, l, i, s, o = `${/*last_progress_level*/
  n[15] * 100}%`, _ = (
    /*progress*/
    n[7] != null && Vt(n)
  );
  return {
    c() {
      e = Q("div"), t = Q("div"), _ && _.c(), l = Y(), i = Q("div"), s = Q("div"), X(t, "class", "progress-level-inner svelte-1txqlrd"), X(s, "class", "progress-bar svelte-1txqlrd"), te(s, "width", o), X(i, "class", "progress-bar-wrap svelte-1txqlrd"), X(e, "class", "progress-level svelte-1txqlrd");
    },
    m(f, a) {
      v(f, e, a), ie(e, t), _ && _.m(t, null), ie(e, l), ie(e, i), ie(i, s), n[30](s);
    },
    p(f, a) {
      /*progress*/
      f[7] != null ? _ ? _.p(f, a) : (_ = Vt(f), _.c(), _.m(t, null)) : _ && (_.d(1), _ = null), a[0] & /*last_progress_level*/
      32768 && o !== (o = `${/*last_progress_level*/
      f[15] * 100}%`) && te(s, "width", o);
    },
    i: Ue,
    o: Ue,
    d(f) {
      f && k(e), _ && _.d(), n[30](null);
    }
  };
}
function Vt(n) {
  let e, t = ze(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = At(Lt(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = pe();
    },
    m(i, s) {
      for (let o = 0; o < l.length; o += 1)
        l[o] && l[o].m(i, s);
      v(i, e, s);
    },
    p(i, s) {
      if (s[0] & /*progress_level, progress*/
      16512) {
        t = ze(
          /*progress*/
          i[7]
        );
        let o;
        for (o = 0; o < t.length; o += 1) {
          const _ = Lt(i, t, o);
          l[o] ? l[o].p(_, s) : (l[o] = At(_), l[o].c(), l[o].m(e.parentNode, e));
        }
        for (; o < l.length; o += 1)
          l[o].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && k(e), Qt(l, i);
    }
  };
}
function Ht(n) {
  let e, t, l, i, s = (
    /*i*/
    n[40] !== 0 && vi()
  ), o = (
    /*p*/
    n[38].desc != null && Nt(n)
  ), _ = (
    /*p*/
    n[38].desc != null && /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[40]
    ] != null && zt()
  ), f = (
    /*progress_level*/
    n[14] != null && Zt(n)
  );
  return {
    c() {
      s && s.c(), e = Y(), o && o.c(), t = Y(), _ && _.c(), l = Y(), f && f.c(), i = pe();
    },
    m(a, r) {
      s && s.m(a, r), v(a, e, r), o && o.m(a, r), v(a, t, r), _ && _.m(a, r), v(a, l, r), f && f.m(a, r), v(a, i, r);
    },
    p(a, r) {
      /*p*/
      a[38].desc != null ? o ? o.p(a, r) : (o = Nt(a), o.c(), o.m(t.parentNode, t)) : o && (o.d(1), o = null), /*p*/
      a[38].desc != null && /*progress_level*/
      a[14] && /*progress_level*/
      a[14][
        /*i*/
        a[40]
      ] != null ? _ || (_ = zt(), _.c(), _.m(l.parentNode, l)) : _ && (_.d(1), _ = null), /*progress_level*/
      a[14] != null ? f ? f.p(a, r) : (f = Zt(a), f.c(), f.m(i.parentNode, i)) : f && (f.d(1), f = null);
    },
    d(a) {
      a && (k(e), k(t), k(l), k(i)), s && s.d(a), o && o.d(a), _ && _.d(a), f && f.d(a);
    }
  };
}
function vi(n) {
  let e;
  return {
    c() {
      e = F(" /");
    },
    m(t, l) {
      v(t, e, l);
    },
    d(t) {
      t && k(e);
    }
  };
}
function Nt(n) {
  let e = (
    /*p*/
    n[38].desc + ""
  ), t;
  return {
    c() {
      t = F(e);
    },
    m(l, i) {
      v(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      l[38].desc + "") && B(t, e);
    },
    d(l) {
      l && k(t);
    }
  };
}
function zt(n) {
  let e;
  return {
    c() {
      e = F("-");
    },
    m(t, l) {
      v(t, e, l);
    },
    d(t) {
      t && k(e);
    }
  };
}
function Zt(n) {
  let e = (100 * /*progress_level*/
  (n[14][
    /*i*/
    n[40]
  ] || 0)).toFixed(1) + "", t, l;
  return {
    c() {
      t = F(e), l = F("%");
    },
    m(i, s) {
      v(i, t, s), v(i, l, s);
    },
    p(i, s) {
      s[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[40]
      ] || 0)).toFixed(1) + "") && B(t, e);
    },
    d(i) {
      i && (k(t), k(l));
    }
  };
}
function At(n) {
  let e, t = (
    /*p*/
    (n[38].desc != null || /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[40]
    ] != null) && Ht(n)
  );
  return {
    c() {
      t && t.c(), e = pe();
    },
    m(l, i) {
      t && t.m(l, i), v(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[38].desc != null || /*progress_level*/
      l[14] && /*progress_level*/
      l[14][
        /*i*/
        l[40]
      ] != null ? t ? t.p(l, i) : (t = Ht(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && k(e), t && t.d(l);
    }
  };
}
function Bt(n) {
  let e, t;
  return {
    c() {
      e = Q("p"), t = F(
        /*loading_text*/
        n[9]
      ), X(e, "class", "loading svelte-1txqlrd");
    },
    m(l, i) {
      v(l, e, i), ie(e, t);
    },
    p(l, i) {
      i[0] & /*loading_text*/
      512 && B(
        t,
        /*loading_text*/
        l[9]
      );
    },
    d(l) {
      l && k(e);
    }
  };
}
function yi(n) {
  let e, t, l, i, s;
  const o = [di, ci], _ = [];
  function f(a, r) {
    return (
      /*status*/
      a[4] === "pending" ? 0 : (
        /*status*/
        a[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = f(n)) && (l = _[t] = o[t](n)), {
    c() {
      e = Q("div"), l && l.c(), X(e, "class", i = "wrap " + /*variant*/
      n[8] + " " + /*show_progress*/
      n[6] + " svelte-1txqlrd"), A(e, "hide", !/*status*/
      n[4] || /*status*/
      n[4] === "complete" || /*show_progress*/
      n[6] === "hidden"), A(
        e,
        "translucent",
        /*variant*/
        n[8] === "center" && /*status*/
        (n[4] === "pending" || /*status*/
        n[4] === "error") || /*translucent*/
        n[11] || /*show_progress*/
        n[6] === "minimal"
      ), A(
        e,
        "generating",
        /*status*/
        n[4] === "generating"
      ), A(
        e,
        "border",
        /*border*/
        n[12]
      ), te(
        e,
        "position",
        /*absolute*/
        n[10] ? "absolute" : "static"
      ), te(
        e,
        "padding",
        /*absolute*/
        n[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(a, r) {
      v(a, e, r), ~t && _[t].m(e, null), n[31](e), s = !0;
    },
    p(a, r) {
      let u = t;
      t = f(a), t === u ? ~t && _[t].p(a, r) : (l && (xt(), we(_[u], 1, 1, () => {
        _[u] = null;
      }), Kt()), ~t ? (l = _[t], l ? l.p(a, r) : (l = _[t] = o[t](a), l.c()), ge(l, 1), l.m(e, null)) : l = null), (!s || r[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      a[8] + " " + /*show_progress*/
      a[6] + " svelte-1txqlrd")) && X(e, "class", i), (!s || r[0] & /*variant, show_progress, status, show_progress*/
      336) && A(e, "hide", !/*status*/
      a[4] || /*status*/
      a[4] === "complete" || /*show_progress*/
      a[6] === "hidden"), (!s || r[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && A(
        e,
        "translucent",
        /*variant*/
        a[8] === "center" && /*status*/
        (a[4] === "pending" || /*status*/
        a[4] === "error") || /*translucent*/
        a[11] || /*show_progress*/
        a[6] === "minimal"
      ), (!s || r[0] & /*variant, show_progress, status*/
      336) && A(
        e,
        "generating",
        /*status*/
        a[4] === "generating"
      ), (!s || r[0] & /*variant, show_progress, border*/
      4416) && A(
        e,
        "border",
        /*border*/
        a[12]
      ), r[0] & /*absolute*/
      1024 && te(
        e,
        "position",
        /*absolute*/
        a[10] ? "absolute" : "static"
      ), r[0] & /*absolute*/
      1024 && te(
        e,
        "padding",
        /*absolute*/
        a[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(a) {
      s || (ge(l), s = !0);
    },
    o(a) {
      we(l), s = !1;
    },
    d(a) {
      a && k(e), ~t && _[t].d(), n[31](null);
    }
  };
}
let Me = [], Oe = !1;
async function Ci(n, e = !0) {
  if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && e !== !0)) {
    if (Me.push(n), !Oe)
      Oe = !0;
    else
      return;
    await ai(), requestAnimationFrame(() => {
      let t = [0, 0];
      for (let l = 0; l < Me.length; l++) {
        const s = Me[l].getBoundingClientRect();
        (l === 0 || s.top + window.scrollY <= t[0]) && (t[0] = s.top + window.scrollY, t[1] = l);
      }
      window.scrollTo({ top: t[0] - 20, behavior: "smooth" }), Oe = !1, Me = [];
    });
  }
}
function qi(n, e, t) {
  let l, { $$slots: i = {}, $$scope: s } = e, { i18n: o } = e, { eta: _ = null } = e, { queue_position: f } = e, { queue_size: a } = e, { status: r } = e, { scroll_to_output: u = !1 } = e, { timer: c = !0 } = e, { show_progress: m = "full" } = e, { message: p = null } = e, { progress: T = null } = e, { variant: L = "default" } = e, { loading_text: S = "Loading..." } = e, { absolute: C = !0 } = e, { translucent: d = !1 } = e, { border: y = !1 } = e, { autoscroll: M } = e, h, P = !1, J = 0, z = 0, D = null, R = null, fe = 0, E = null, K, Z = null, _e = !0;
  const g = () => {
    t(0, _ = t(26, D = t(19, ae = null))), t(24, J = performance.now()), t(25, z = 0), P = !0, qe();
  };
  function qe() {
    requestAnimationFrame(() => {
      t(25, z = (performance.now() - J) / 1e3), P && qe();
    });
  }
  function Le() {
    t(25, z = 0), t(0, _ = t(26, D = t(19, ae = null))), P && (P = !1);
  }
  ri(() => {
    P && Le();
  });
  let ae = null;
  function Ze(w) {
    Ct[w ? "unshift" : "push"](() => {
      Z = w, t(16, Z), t(7, T), t(14, E), t(15, K);
    });
  }
  function Ae(w) {
    Ct[w ? "unshift" : "push"](() => {
      h = w, t(13, h);
    });
  }
  return n.$$set = (w) => {
    "i18n" in w && t(1, o = w.i18n), "eta" in w && t(0, _ = w.eta), "queue_position" in w && t(2, f = w.queue_position), "queue_size" in w && t(3, a = w.queue_size), "status" in w && t(4, r = w.status), "scroll_to_output" in w && t(21, u = w.scroll_to_output), "timer" in w && t(5, c = w.timer), "show_progress" in w && t(6, m = w.show_progress), "message" in w && t(22, p = w.message), "progress" in w && t(7, T = w.progress), "variant" in w && t(8, L = w.variant), "loading_text" in w && t(9, S = w.loading_text), "absolute" in w && t(10, C = w.absolute), "translucent" in w && t(11, d = w.translucent), "border" in w && t(12, y = w.border), "autoscroll" in w && t(23, M = w.autoscroll), "$$scope" in w && t(28, s = w.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    218103809 && (_ === null && t(0, _ = D), _ != null && D !== _ && (t(27, R = (performance.now() - J) / 1e3 + _), t(19, ae = R.toFixed(1)), t(26, D = _))), n.$$.dirty[0] & /*eta_from_start, timer_diff*/
    167772160 && t(17, fe = R === null || R <= 0 || !z ? null : Math.min(z / R, 1)), n.$$.dirty[0] & /*progress*/
    128 && T != null && t(18, _e = !1), n.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (T != null ? t(14, E = T.map((w) => {
      if (w.index != null && w.length != null)
        return w.index / w.length;
      if (w.progress != null)
        return w.progress;
    })) : t(14, E = null), E ? (t(15, K = E[E.length - 1]), Z && (K === 0 ? t(16, Z.style.transition = "0", Z) : t(16, Z.style.transition = "150ms", Z))) : t(15, K = void 0)), n.$$.dirty[0] & /*status*/
    16 && (r === "pending" ? g() : Le()), n.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    10493968 && h && u && (r === "pending" || r === "complete") && Ci(h, M), n.$$.dirty[0] & /*status, message*/
    4194320, n.$$.dirty[0] & /*timer_diff*/
    33554432 && t(20, l = z.toFixed(1));
  }, [
    _,
    o,
    f,
    a,
    r,
    c,
    m,
    T,
    L,
    S,
    C,
    d,
    y,
    h,
    E,
    K,
    Z,
    fe,
    _e,
    ae,
    l,
    u,
    p,
    M,
    J,
    z,
    D,
    R,
    s,
    i,
    Ze,
    Ae
  ];
}
class Li extends $n {
  constructor(e) {
    super(), si(
      this,
      e,
      qi,
      yi,
      fi,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 21,
        timer: 5,
        show_progress: 6,
        message: 22,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 23
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: Si,
  add_flush_callback: Pt,
  assign: Ti,
  bind: Dt,
  binding_callbacks: Et,
  check_outros: Fi,
  create_component: Qe,
  destroy_component: xe,
  detach: Mi,
  flush: j,
  get_spread_object: ji,
  get_spread_update: Vi,
  group_outros: Hi,
  init: Ni,
  insert: zi,
  mount_component: $e,
  safe_not_equal: Zi,
  space: Ai,
  transition_in: be,
  transition_out: Ce
} = window.__gradio__svelte__internal;
function It(n) {
  let e, t;
  const l = [
    { autoscroll: (
      /*gradio*/
      n[3].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      n[3].i18n
    ) },
    /*loading_status*/
    n[17]
  ];
  let i = {};
  for (let s = 0; s < l.length; s += 1)
    i = Ti(i, l[s]);
  return e = new Li({ props: i }), {
    c() {
      Qe(e.$$.fragment);
    },
    m(s, o) {
      $e(e, s, o), t = !0;
    },
    p(s, o) {
      const _ = o & /*gradio, loading_status*/
      131080 ? Vi(l, [
        o & /*gradio*/
        8 && { autoscroll: (
          /*gradio*/
          s[3].autoscroll
        ) },
        o & /*gradio*/
        8 && { i18n: (
          /*gradio*/
          s[3].i18n
        ) },
        o & /*loading_status*/
        131072 && ji(
          /*loading_status*/
          s[17]
        )
      ]) : {};
      e.$set(_);
    },
    i(s) {
      t || (be(e.$$.fragment, s), t = !0);
    },
    o(s) {
      Ce(e.$$.fragment, s), t = !1;
    },
    d(s) {
      xe(e, s);
    }
  };
}
function Bi(n) {
  let e, t, l, i, s, o = (
    /*loading_status*/
    n[17] && It(n)
  );
  function _(r) {
    n[22](r);
  }
  function f(r) {
    n[23](r);
  }
  let a = {
    label: (
      /*label*/
      n[4]
    ),
    info: (
      /*info*/
      n[6]
    ),
    show_label: (
      /*show_label*/
      n[10]
    ),
    show_legend: (
      /*show_legend*/
      n[11]
    ),
    show_legend_label: (
      /*show_legend_label*/
      n[12]
    ),
    legend_label: (
      /*legend_label*/
      n[5]
    ),
    color_map: (
      /*color_map*/
      n[1]
    ),
    show_copy_button: (
      /*show_copy_button*/
      n[16]
    ),
    container: (
      /*container*/
      n[13]
    ),
    disabled: !/*interactive*/
    n[18]
  };
  return (
    /*value*/
    n[0] !== void 0 && (a.value = /*value*/
    n[0]), /*value_is_output*/
    n[2] !== void 0 && (a.value_is_output = /*value_is_output*/
    n[2]), t = new On({ props: a }), Et.push(() => Dt(t, "value", _)), Et.push(() => Dt(t, "value_is_output", f)), t.$on(
      "change",
      /*change_handler*/
      n[24]
    ), t.$on(
      "input",
      /*input_handler*/
      n[25]
    ), t.$on(
      "submit",
      /*submit_handler*/
      n[26]
    ), t.$on(
      "blur",
      /*blur_handler*/
      n[27]
    ), t.$on(
      "select",
      /*select_handler*/
      n[28]
    ), t.$on(
      "focus",
      /*focus_handler*/
      n[29]
    ), {
      c() {
        o && o.c(), e = Ai(), Qe(t.$$.fragment);
      },
      m(r, u) {
        o && o.m(r, u), zi(r, e, u), $e(t, r, u), s = !0;
      },
      p(r, u) {
        /*loading_status*/
        r[17] ? o ? (o.p(r, u), u & /*loading_status*/
        131072 && be(o, 1)) : (o = It(r), o.c(), be(o, 1), o.m(e.parentNode, e)) : o && (Hi(), Ce(o, 1, 1, () => {
          o = null;
        }), Fi());
        const c = {};
        u & /*label*/
        16 && (c.label = /*label*/
        r[4]), u & /*info*/
        64 && (c.info = /*info*/
        r[6]), u & /*show_label*/
        1024 && (c.show_label = /*show_label*/
        r[10]), u & /*show_legend*/
        2048 && (c.show_legend = /*show_legend*/
        r[11]), u & /*show_legend_label*/
        4096 && (c.show_legend_label = /*show_legend_label*/
        r[12]), u & /*legend_label*/
        32 && (c.legend_label = /*legend_label*/
        r[5]), u & /*color_map*/
        2 && (c.color_map = /*color_map*/
        r[1]), u & /*show_copy_button*/
        65536 && (c.show_copy_button = /*show_copy_button*/
        r[16]), u & /*container*/
        8192 && (c.container = /*container*/
        r[13]), u & /*interactive*/
        262144 && (c.disabled = !/*interactive*/
        r[18]), !l && u & /*value*/
        1 && (l = !0, c.value = /*value*/
        r[0], Pt(() => l = !1)), !i && u & /*value_is_output*/
        4 && (i = !0, c.value_is_output = /*value_is_output*/
        r[2], Pt(() => i = !1)), t.$set(c);
      },
      i(r) {
        s || (be(o), be(t.$$.fragment, r), s = !0);
      },
      o(r) {
        Ce(o), Ce(t.$$.fragment, r), s = !1;
      },
      d(r) {
        r && Mi(e), o && o.d(r), xe(t, r);
      }
    }
  );
}
function Pi(n) {
  let e, t;
  return e = new bl({
    props: {
      visible: (
        /*visible*/
        n[9]
      ),
      elem_id: (
        /*elem_id*/
        n[7]
      ),
      elem_classes: (
        /*elem_classes*/
        n[8]
      ),
      scale: (
        /*scale*/
        n[14]
      ),
      min_width: (
        /*min_width*/
        n[15]
      ),
      allow_overflow: !1,
      padding: (
        /*container*/
        n[13]
      ),
      $$slots: { default: [Bi] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      Qe(e.$$.fragment);
    },
    m(l, i) {
      $e(e, l, i), t = !0;
    },
    p(l, [i]) {
      const s = {};
      i & /*visible*/
      512 && (s.visible = /*visible*/
      l[9]), i & /*elem_id*/
      128 && (s.elem_id = /*elem_id*/
      l[7]), i & /*elem_classes*/
      256 && (s.elem_classes = /*elem_classes*/
      l[8]), i & /*scale*/
      16384 && (s.scale = /*scale*/
      l[14]), i & /*min_width*/
      32768 && (s.min_width = /*min_width*/
      l[15]), i & /*container*/
      8192 && (s.padding = /*container*/
      l[13]), i & /*$$scope, label, info, show_label, show_legend, show_legend_label, legend_label, color_map, show_copy_button, container, interactive, value, value_is_output, gradio, loading_status*/
      1074216063 && (s.$$scope = { dirty: i, ctx: l }), e.$set(s);
    },
    i(l) {
      t || (be(e.$$.fragment, l), t = !0);
    },
    o(l) {
      Ce(e.$$.fragment, l), t = !1;
    },
    d(l) {
      xe(e, l);
    }
  };
}
function Di(n, e, t) {
  let { gradio: l } = e, { label: i = "Highlighted Textbox" } = e, { legend_label: s = "Highlights:" } = e, { info: o = void 0 } = e, { elem_id: _ = "" } = e, { elem_classes: f = [] } = e, { visible: a = !0 } = e, { value: r } = e, { show_label: u } = e, { show_legend: c } = e, { show_legend_label: m } = e, { color_map: p = {} } = e, { container: T = !0 } = e, { scale: L = null } = e, { min_width: S = void 0 } = e, { show_copy_button: C = !1 } = e, { loading_status: d = void 0 } = e, { value_is_output: y = !1 } = e, { combine_adjacent: M = !1 } = e, { interactive: h = !0 } = e;
  const P = !1, J = !0;
  function z(g) {
    r = g, t(0, r), t(19, M);
  }
  function D(g) {
    y = g, t(2, y);
  }
  const R = () => l.dispatch("change"), fe = () => l.dispatch("input"), E = () => l.dispatch("submit"), K = () => l.dispatch("blur"), Z = (g) => l.dispatch("select", g.detail), _e = () => l.dispatch("focus");
  return n.$$set = (g) => {
    "gradio" in g && t(3, l = g.gradio), "label" in g && t(4, i = g.label), "legend_label" in g && t(5, s = g.legend_label), "info" in g && t(6, o = g.info), "elem_id" in g && t(7, _ = g.elem_id), "elem_classes" in g && t(8, f = g.elem_classes), "visible" in g && t(9, a = g.visible), "value" in g && t(0, r = g.value), "show_label" in g && t(10, u = g.show_label), "show_legend" in g && t(11, c = g.show_legend), "show_legend_label" in g && t(12, m = g.show_legend_label), "color_map" in g && t(1, p = g.color_map), "container" in g && t(13, T = g.container), "scale" in g && t(14, L = g.scale), "min_width" in g && t(15, S = g.min_width), "show_copy_button" in g && t(16, C = g.show_copy_button), "loading_status" in g && t(17, d = g.loading_status), "value_is_output" in g && t(2, y = g.value_is_output), "combine_adjacent" in g && t(19, M = g.combine_adjacent), "interactive" in g && t(18, h = g.interactive);
  }, n.$$.update = () => {
    n.$$.dirty & /*color_map*/
    2 && !p && Object.keys(p).length && t(1, p), n.$$.dirty & /*value, combine_adjacent*/
    524289 && r && M && t(0, r = Cn(r, "equal"));
  }, [
    r,
    p,
    y,
    l,
    i,
    s,
    o,
    _,
    f,
    a,
    u,
    c,
    m,
    T,
    L,
    S,
    C,
    d,
    h,
    M,
    P,
    J,
    z,
    D,
    R,
    fe,
    E,
    K,
    Z,
    _e
  ];
}
class Ii extends Si {
  constructor(e) {
    super(), Ni(this, e, Di, Pi, Zi, {
      gradio: 3,
      label: 4,
      legend_label: 5,
      info: 6,
      elem_id: 7,
      elem_classes: 8,
      visible: 9,
      value: 0,
      show_label: 10,
      show_legend: 11,
      show_legend_label: 12,
      color_map: 1,
      container: 13,
      scale: 14,
      min_width: 15,
      show_copy_button: 16,
      loading_status: 17,
      value_is_output: 2,
      combine_adjacent: 19,
      interactive: 18,
      autofocus: 20,
      autoscroll: 21
    });
  }
  get gradio() {
    return this.$$.ctx[3];
  }
  set gradio(e) {
    this.$$set({ gradio: e }), j();
  }
  get label() {
    return this.$$.ctx[4];
  }
  set label(e) {
    this.$$set({ label: e }), j();
  }
  get legend_label() {
    return this.$$.ctx[5];
  }
  set legend_label(e) {
    this.$$set({ legend_label: e }), j();
  }
  get info() {
    return this.$$.ctx[6];
  }
  set info(e) {
    this.$$set({ info: e }), j();
  }
  get elem_id() {
    return this.$$.ctx[7];
  }
  set elem_id(e) {
    this.$$set({ elem_id: e }), j();
  }
  get elem_classes() {
    return this.$$.ctx[8];
  }
  set elem_classes(e) {
    this.$$set({ elem_classes: e }), j();
  }
  get visible() {
    return this.$$.ctx[9];
  }
  set visible(e) {
    this.$$set({ visible: e }), j();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({ value: e }), j();
  }
  get show_label() {
    return this.$$.ctx[10];
  }
  set show_label(e) {
    this.$$set({ show_label: e }), j();
  }
  get show_legend() {
    return this.$$.ctx[11];
  }
  set show_legend(e) {
    this.$$set({ show_legend: e }), j();
  }
  get show_legend_label() {
    return this.$$.ctx[12];
  }
  set show_legend_label(e) {
    this.$$set({ show_legend_label: e }), j();
  }
  get color_map() {
    return this.$$.ctx[1];
  }
  set color_map(e) {
    this.$$set({ color_map: e }), j();
  }
  get container() {
    return this.$$.ctx[13];
  }
  set container(e) {
    this.$$set({ container: e }), j();
  }
  get scale() {
    return this.$$.ctx[14];
  }
  set scale(e) {
    this.$$set({ scale: e }), j();
  }
  get min_width() {
    return this.$$.ctx[15];
  }
  set min_width(e) {
    this.$$set({ min_width: e }), j();
  }
  get show_copy_button() {
    return this.$$.ctx[16];
  }
  set show_copy_button(e) {
    this.$$set({ show_copy_button: e }), j();
  }
  get loading_status() {
    return this.$$.ctx[17];
  }
  set loading_status(e) {
    this.$$set({ loading_status: e }), j();
  }
  get value_is_output() {
    return this.$$.ctx[2];
  }
  set value_is_output(e) {
    this.$$set({ value_is_output: e }), j();
  }
  get combine_adjacent() {
    return this.$$.ctx[19];
  }
  set combine_adjacent(e) {
    this.$$set({ combine_adjacent: e }), j();
  }
  get interactive() {
    return this.$$.ctx[18];
  }
  set interactive(e) {
    this.$$set({ interactive: e }), j();
  }
  get autofocus() {
    return this.$$.ctx[20];
  }
  get autoscroll() {
    return this.$$.ctx[21];
  }
}
export {
  Ii as default
};

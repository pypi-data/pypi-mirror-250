import{I as s,i$ as S,v as l,a3 as I,j0 as N,ac as R,j1 as T,j2 as z,j3 as V,j4 as A,j5 as F,j6 as G,j7 as _,as as D,j8 as K,j9 as W}from"./index-58ecvHlx.js";import{E as H}from"./chunk-VMD3UMGK-uvnz6tkL.js";var P=String.raw,E=P`
  :root,
  :host {
    --chakra-vh: 100vh;
  }

  @supports (height: -webkit-fill-available) {
    :root,
    :host {
      --chakra-vh: -webkit-fill-available;
    }
  }

  @supports (height: -moz-fill-available) {
    :root,
    :host {
      --chakra-vh: -moz-fill-available;
    }
  }

  @supports (height: 100dvh) {
    :root,
    :host {
      --chakra-vh: 100dvh;
    }
  }
`,U=()=>s.jsx(S,{styles:E}),Y=({scope:e=""})=>s.jsx(S,{styles:P`
      html {
        line-height: 1.5;
        -webkit-text-size-adjust: 100%;
        font-family: system-ui, sans-serif;
        -webkit-font-smoothing: antialiased;
        text-rendering: optimizeLegibility;
        -moz-osx-font-smoothing: grayscale;
        touch-action: manipulation;
      }

      body {
        position: relative;
        min-height: 100%;
        margin: 0;
        font-feature-settings: "kern";
      }

      ${e} :where(*, *::before, *::after) {
        border-width: 0;
        border-style: solid;
        box-sizing: border-box;
        word-wrap: break-word;
      }

      main {
        display: block;
      }

      ${e} hr {
        border-top-width: 1px;
        box-sizing: content-box;
        height: 0;
        overflow: visible;
      }

      ${e} :where(pre, code, kbd,samp) {
        font-family: SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 1em;
      }

      ${e} a {
        background-color: transparent;
        color: inherit;
        text-decoration: inherit;
      }

      ${e} abbr[title] {
        border-bottom: none;
        text-decoration: underline;
        -webkit-text-decoration: underline dotted;
        text-decoration: underline dotted;
      }

      ${e} :where(b, strong) {
        font-weight: bold;
      }

      ${e} small {
        font-size: 80%;
      }

      ${e} :where(sub,sup) {
        font-size: 75%;
        line-height: 0;
        position: relative;
        vertical-align: baseline;
      }

      ${e} sub {
        bottom: -0.25em;
      }

      ${e} sup {
        top: -0.5em;
      }

      ${e} img {
        border-style: none;
      }

      ${e} :where(button, input, optgroup, select, textarea) {
        font-family: inherit;
        font-size: 100%;
        line-height: 1.15;
        margin: 0;
      }

      ${e} :where(button, input) {
        overflow: visible;
      }

      ${e} :where(button, select) {
        text-transform: none;
      }

      ${e} :where(
          button::-moz-focus-inner,
          [type="button"]::-moz-focus-inner,
          [type="reset"]::-moz-focus-inner,
          [type="submit"]::-moz-focus-inner
        ) {
        border-style: none;
        padding: 0;
      }

      ${e} fieldset {
        padding: 0.35em 0.75em 0.625em;
      }

      ${e} legend {
        box-sizing: border-box;
        color: inherit;
        display: table;
        max-width: 100%;
        padding: 0;
        white-space: normal;
      }

      ${e} progress {
        vertical-align: baseline;
      }

      ${e} textarea {
        overflow: auto;
      }

      ${e} :where([type="checkbox"], [type="radio"]) {
        box-sizing: border-box;
        padding: 0;
      }

      ${e} input[type="number"]::-webkit-inner-spin-button,
      ${e} input[type="number"]::-webkit-outer-spin-button {
        -webkit-appearance: none !important;
      }

      ${e} input[type="number"] {
        -moz-appearance: textfield;
      }

      ${e} input[type="search"] {
        -webkit-appearance: textfield;
        outline-offset: -2px;
      }

      ${e} input[type="search"]::-webkit-search-decoration {
        -webkit-appearance: none !important;
      }

      ${e} ::-webkit-file-upload-button {
        -webkit-appearance: button;
        font: inherit;
      }

      ${e} details {
        display: block;
      }

      ${e} summary {
        display: list-item;
      }

      template {
        display: none;
      }

      [hidden] {
        display: none !important;
      }

      ${e} :where(
          blockquote,
          dl,
          dd,
          h1,
          h2,
          h3,
          h4,
          h5,
          h6,
          hr,
          figure,
          p,
          pre
        ) {
        margin: 0;
      }

      ${e} button {
        background: transparent;
        padding: 0;
      }

      ${e} fieldset {
        margin: 0;
        padding: 0;
      }

      ${e} :where(ol, ul) {
        margin: 0;
        padding: 0;
      }

      ${e} textarea {
        resize: vertical;
      }

      ${e} :where(button, [role="button"]) {
        cursor: pointer;
      }

      ${e} button::-moz-focus-inner {
        border: 0 !important;
      }

      ${e} table {
        border-collapse: collapse;
      }

      ${e} :where(h1, h2, h3, h4, h5, h6) {
        font-size: inherit;
        font-weight: inherit;
      }

      ${e} :where(button, input, optgroup, select, textarea) {
        padding: 0;
        line-height: inherit;
        color: inherit;
      }

      ${e} :where(img, svg, video, canvas, audio, iframe, embed, object) {
        display: block;
      }

      ${e} :where(img, video) {
        max-width: 100%;
        height: auto;
      }

      [data-js-focus-visible]
        :focus:not([data-focus-visible-added]):not(
          [data-focus-visible-disabled]
        ) {
        outline: none;
        box-shadow: none;
      }

      ${e} select::-ms-expand {
        display: none;
      }

      ${E}
    `}),p={light:"chakra-ui-light",dark:"chakra-ui-dark"};function Z(e={}){const{preventTransition:r=!0}=e,n={setDataset:t=>{const o=r?n.preventTransition():void 0;document.documentElement.dataset.theme=t,document.documentElement.style.colorScheme=t,o==null||o()},setClassName(t){document.body.classList.add(t?p.dark:p.light),document.body.classList.remove(t?p.light:p.dark)},query(){return window.matchMedia("(prefers-color-scheme: dark)")},getSystemTheme(t){var o;return((o=n.query().matches)!=null?o:t==="dark")?"dark":"light"},addListener(t){const o=n.query(),i=a=>{t(a.matches?"dark":"light")};return typeof o.addListener=="function"?o.addListener(i):o.addEventListener("change",i),()=>{typeof o.removeListener=="function"?o.removeListener(i):o.removeEventListener("change",i)}},preventTransition(){const t=document.createElement("style");return t.appendChild(document.createTextNode("*{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}")),document.head.appendChild(t),()=>{window.getComputedStyle(document.body),requestAnimationFrame(()=>{requestAnimationFrame(()=>{document.head.removeChild(t)})})}}};return n}var B="chakra-ui-color-mode";function J(e){return{ssr:!1,type:"localStorage",get(r){if(!(globalThis!=null&&globalThis.document))return r;let n;try{n=localStorage.getItem(e)||r}catch{}return n||r},set(r){try{localStorage.setItem(e,r)}catch{}}}}var Q=J(B),j=()=>{};function M(e,r){return e.type==="cookie"&&e.ssr?e.get(r):r}function L(e){const{value:r,children:n,options:{useSystemColorMode:t,initialColorMode:o,disableTransitionOnChange:i}={},colorModeManager:a=Q}=e,u=o==="dark"?"dark":"light",[c,v]=l.useState(()=>M(a,u)),[y,b]=l.useState(()=>M(a)),{getSystemTheme:k,setClassName:w,setDataset:x,addListener:$}=l.useMemo(()=>Z({preventTransition:i}),[i]),f=o==="system"&&!c?y:c,d=l.useCallback(h=>{const g=h==="system"?k():h;v(g),w(g==="dark"),x(g),a.set(g)},[a,k,w,x]);I(()=>{o==="system"&&b(k())},[]),l.useEffect(()=>{const h=a.get();if(h){d(h);return}if(o==="system"){d("system");return}d(u)},[a,u,o,d]);const C=l.useCallback(()=>{d(f==="dark"?"light":"dark")},[f,d]);l.useEffect(()=>{if(t)return $(d)},[t,$,d]);const q=l.useMemo(()=>({colorMode:r??f,toggleColorMode:r?j:C,setColorMode:r?j:d,forced:r!==void 0}),[f,C,d,r]);return s.jsx(N.Provider,{value:q,children:n})}L.displayName="ColorModeProvider";var X=["borders","breakpoints","colors","components","config","direction","fonts","fontSizes","fontWeights","letterSpacings","lineHeights","radii","shadows","sizes","space","styles","transition","zIndices"];function ee(e){return R(e)?X.every(r=>Object.prototype.hasOwnProperty.call(e,r)):!1}function m(e){return typeof e=="function"}function te(...e){return r=>e.reduce((n,t)=>t(n),r)}var re=e=>function(...n){let t=[...n],o=n[n.length-1];return ee(o)&&t.length>1?t=t.slice(0,t.length-1):o=e,te(...t.map(i=>a=>m(i)?i(a):ne(a,i)))(o)},oe=re(z);function ne(...e){return T({},...e,O)}function O(e,r,n,t){if((m(e)||m(r))&&Object.prototype.hasOwnProperty.call(t,n))return(...o)=>{const i=m(e)?e(...o):e,a=m(r)?r(...o):r;return T({},i,a,O)}}var ie=e=>{const{children:r,colorModeManager:n,portalZIndex:t,resetScope:o,resetCSS:i=!0,theme:a={},environment:u,cssVarsRoot:c,disableEnvironment:v,disableGlobalStyle:y}=e,b=s.jsx(H,{environment:u,disabled:v,children:r});return s.jsx(V,{theme:a,cssVarsRoot:c,children:s.jsxs(L,{colorModeManager:n,options:a.config,children:[i?s.jsx(Y,{scope:o}):s.jsx(U,{}),!y&&s.jsx(A,{}),t?s.jsx(F,{zIndex:t,children:b}):b]})})},ae=e=>function({children:n,theme:t=e,toastOptions:o,...i}){return s.jsxs(ie,{theme:t,...i,children:[s.jsx(G,{value:o==null?void 0:o.defaultOptions,children:n}),s.jsx(_,{...o})]})},se=ae(z);function le({children:e}){const{i18n:r}=D(),n=r.dir(),t=l.useMemo(()=>oe({...K,direction:n}),[n]);return l.useEffect(()=>{document.body.dir=n},[n]),s.jsx(se,{theme:t,toastOptions:W,children:e})}const he=l.memo(le);export{he as default};

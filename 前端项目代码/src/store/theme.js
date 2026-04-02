import { defineStore } from 'pinia';

const createTheme = (name, config) => ({
  name,
  ...config
});

export const useThemeStore = defineStore('theme', {
  state: () => ({
    currentTheme: localStorage.getItem('theme') || 'light',
    themes: {
      light: createTheme('曜石金刊', {
        pageBg: '#111315',
        pageBgSecondary: '#1a1d20',
        surfaceBase: 'rgba(28, 31, 35, 0.88)',
        surfaceElevated: 'rgba(35, 38, 43, 0.94)',
        surfaceOverlay: 'rgba(20, 22, 25, 0.82)',
        secondaryColor: 'rgba(191, 153, 86, 0.12)',
        textPrimary: '#f5f1e8',
        textSecondary: 'rgba(228, 220, 206, 0.72)',
        textMuted: 'rgba(193, 183, 167, 0.5)',
        accentPrimary: '#c89b53',
        accentSecondary: '#9f6f3d',
        accentSoft: 'rgba(200, 155, 83, 0.12)',
        accentGlow: 'rgba(200, 155, 83, 0.16)',
        accentGlowStrong: 'rgba(159, 111, 61, 0.18)',
        borderSubtle: 'rgba(255, 255, 255, 0.07)',
        borderStrong: 'rgba(200, 155, 83, 0.24)',
        shadowSoft: '0 18px 40px rgba(0, 0, 0, 0.26)',
        shadowGlow: '0 10px 24px rgba(0, 0, 0, 0.16)',
        shadowGlowStrong: '0 14px 32px rgba(0, 0, 0, 0.2)',
        navBackground: 'rgba(24, 27, 31, 0.88)',
        navBorder: 'rgba(255, 255, 255, 0.06)',
        tabActive: '#ddb26f',
        tabInactive: 'rgba(221, 214, 202, 0.48)',
        buttonPrimaryBg: 'linear-gradient(135deg, #aa7c45 0%, #d1a35e 100%)',
        buttonPrimaryText: '#16110b',
        buttonGhostBorder: 'rgba(255, 255, 255, 0.08)',
        buttonGhostGlow: 'rgba(200, 155, 83, 0.12)',
        orbColorA: 'rgba(111, 88, 58, 0.12)',
        orbColorB: 'rgba(200, 155, 83, 0.08)',
        lineColor: 'rgba(255, 255, 255, 0.03)',
        gridColor: 'rgba(255, 255, 255, 0.02)',
        backdropBlur: '20px',
        panelOpacity: '0.94',
        backgroundColor: '#111315',
        textColor: '#f5f1e8',
        primaryColor: '#c89b53'
      }),
      dark: createTheme('深夜社论', {
        pageBg: '#0e1012',
        pageBgSecondary: '#17191c',
        surfaceBase: 'rgba(24, 26, 30, 0.9)',
        surfaceElevated: 'rgba(31, 34, 39, 0.95)',
        surfaceOverlay: 'rgba(18, 20, 23, 0.84)',
        secondaryColor: 'rgba(181, 129, 76, 0.1)',
        textPrimary: '#f3efe8',
        textSecondary: 'rgba(226, 218, 205, 0.7)',
        textMuted: 'rgba(191, 182, 167, 0.48)',
        accentPrimary: '#bb8749',
        accentSecondary: '#8f6337',
        accentSoft: 'rgba(187, 135, 73, 0.11)',
        accentGlow: 'rgba(187, 135, 73, 0.14)',
        accentGlowStrong: 'rgba(143, 99, 55, 0.18)',
        borderSubtle: 'rgba(255, 255, 255, 0.06)',
        borderStrong: 'rgba(187, 135, 73, 0.22)',
        shadowSoft: '0 20px 44px rgba(0, 0, 0, 0.28)',
        shadowGlow: '0 10px 24px rgba(0, 0, 0, 0.18)',
        shadowGlowStrong: '0 16px 36px rgba(0, 0, 0, 0.22)',
        navBackground: 'rgba(20, 22, 25, 0.9)',
        navBorder: 'rgba(255, 255, 255, 0.05)',
        tabActive: '#d1a15f',
        tabInactive: 'rgba(220, 213, 201, 0.46)',
        buttonPrimaryBg: 'linear-gradient(135deg, #9f7343 0%, #c89353 100%)',
        buttonPrimaryText: '#15100a',
        buttonGhostBorder: 'rgba(255, 255, 255, 0.08)',
        buttonGhostGlow: 'rgba(187, 135, 73, 0.1)',
        orbColorA: 'rgba(122, 89, 50, 0.1)',
        orbColorB: 'rgba(187, 135, 73, 0.07)',
        lineColor: 'rgba(255, 255, 255, 0.025)',
        gridColor: 'rgba(255, 255, 255, 0.016)',
        backdropBlur: '20px',
        panelOpacity: '0.95',
        backgroundColor: '#0e1012',
        textColor: '#f3efe8',
        primaryColor: '#bb8749'
      }),
      blue: createTheme('石墨蓝刊', {
        pageBg: '#0d1114',
        pageBgSecondary: '#161d22',
        surfaceBase: 'rgba(21, 28, 33, 0.9)',
        surfaceElevated: 'rgba(29, 36, 42, 0.95)',
        surfaceOverlay: 'rgba(16, 21, 25, 0.84)',
        secondaryColor: 'rgba(114, 138, 163, 0.12)',
        textPrimary: '#edf0f2',
        textSecondary: 'rgba(212, 219, 224, 0.7)',
        textMuted: 'rgba(171, 182, 190, 0.48)',
        accentPrimary: '#be9155',
        accentSecondary: '#76889c',
        accentSoft: 'rgba(190, 145, 85, 0.11)',
        accentGlow: 'rgba(190, 145, 85, 0.14)',
        accentGlowStrong: 'rgba(118, 136, 156, 0.16)',
        borderSubtle: 'rgba(255, 255, 255, 0.06)',
        borderStrong: 'rgba(190, 145, 85, 0.2)',
        shadowSoft: '0 20px 40px rgba(0, 0, 0, 0.26)',
        shadowGlow: '0 10px 22px rgba(0, 0, 0, 0.16)',
        shadowGlowStrong: '0 16px 32px rgba(0, 0, 0, 0.2)',
        navBackground: 'rgba(18, 23, 27, 0.9)',
        navBorder: 'rgba(255, 255, 255, 0.05)',
        tabActive: '#d1a86d',
        tabInactive: 'rgba(210, 217, 223, 0.46)',
        buttonPrimaryBg: 'linear-gradient(135deg, #7c8ea1 0%, #be9155 100%)',
        buttonPrimaryText: '#111315',
        buttonGhostBorder: 'rgba(255, 255, 255, 0.08)',
        buttonGhostGlow: 'rgba(190, 145, 85, 0.08)',
        orbColorA: 'rgba(91, 107, 121, 0.1)',
        orbColorB: 'rgba(190, 145, 85, 0.06)',
        lineColor: 'rgba(255, 255, 255, 0.025)',
        gridColor: 'rgba(255, 255, 255, 0.018)',
        backdropBlur: '20px',
        panelOpacity: '0.95',
        backgroundColor: '#0d1114',
        textColor: '#edf0f2',
        primaryColor: '#be9155'
      }),
      green: createTheme('琥珀周刊', {
        pageBg: '#120f0c',
        pageBgSecondary: '#1e1915',
        surfaceBase: 'rgba(31, 26, 21, 0.9)',
        surfaceElevated: 'rgba(38, 32, 26, 0.95)',
        surfaceOverlay: 'rgba(23, 19, 16, 0.84)',
        secondaryColor: 'rgba(174, 132, 83, 0.12)',
        textPrimary: '#f6f0e7',
        textSecondary: 'rgba(231, 220, 205, 0.72)',
        textMuted: 'rgba(197, 184, 168, 0.5)',
        accentPrimary: '#cf9453',
        accentSecondary: '#926745',
        accentSoft: 'rgba(207, 148, 83, 0.12)',
        accentGlow: 'rgba(207, 148, 83, 0.14)',
        accentGlowStrong: 'rgba(146, 103, 69, 0.18)',
        borderSubtle: 'rgba(255, 255, 255, 0.06)',
        borderStrong: 'rgba(207, 148, 83, 0.22)',
        shadowSoft: '0 20px 42px rgba(0, 0, 0, 0.28)',
        shadowGlow: '0 10px 24px rgba(0, 0, 0, 0.16)',
        shadowGlowStrong: '0 16px 34px rgba(0, 0, 0, 0.2)',
        navBackground: 'rgba(26, 22, 18, 0.9)',
        navBorder: 'rgba(255, 255, 255, 0.05)',
        tabActive: '#ddb075',
        tabInactive: 'rgba(226, 214, 199, 0.46)',
        buttonPrimaryBg: 'linear-gradient(135deg, #996c44 0%, #cf9453 100%)',
        buttonPrimaryText: '#17110b',
        buttonGhostBorder: 'rgba(255, 255, 255, 0.08)',
        buttonGhostGlow: 'rgba(207, 148, 83, 0.1)',
        orbColorA: 'rgba(133, 94, 59, 0.1)',
        orbColorB: 'rgba(207, 148, 83, 0.07)',
        lineColor: 'rgba(255, 255, 255, 0.024)',
        gridColor: 'rgba(255, 255, 255, 0.016)',
        backdropBlur: '20px',
        panelOpacity: '0.95',
        backgroundColor: '#120f0c',
        textColor: '#f6f0e7',
        primaryColor: '#cf9453'
      })
    }
  }),

  getters: {
    getCurrentTheme: (state) => state.currentTheme,
    getThemeConfig: (state) => state.themes[state.currentTheme],
    getAllThemes: (state) => Object.keys(state.themes).map((key) => ({
      id: key,
      name: state.themes[key].name,
      primaryColor: state.themes[key].accentPrimary,
      secondaryColor: state.themes[key].accentSecondary,
      pageBg: state.themes[key].pageBg,
      pageBgSecondary: state.themes[key].pageBgSecondary,
      lineColor: state.themes[key].lineColor,
      surfaceBase: state.themes[key].surfaceBase
    }))
  },

  actions: {
    setTheme(themeName) {
      if (this.themes[themeName]) {
        this.currentTheme = themeName;
        localStorage.setItem('theme', themeName);
        this.applyTheme();
      }
    },

    applyTheme() {
      const theme = this.themes[this.currentTheme];
      const root = document.documentElement;

      Object.entries({
        '--page-bg': theme.pageBg,
        '--page-bg-secondary': theme.pageBgSecondary,
        '--surface-base': theme.surfaceBase,
        '--surface-elevated': theme.surfaceElevated,
        '--surface-overlay': theme.surfaceOverlay,
        '--text-primary': theme.textPrimary,
        '--text-secondary': theme.textSecondary,
        '--text-muted': theme.textMuted,
        '--accent-primary': theme.accentPrimary,
        '--accent-secondary': theme.accentSecondary,
        '--accent-soft': theme.accentSoft,
        '--accent-glow': theme.accentGlow,
        '--accent-glow-strong': theme.accentGlowStrong,
        '--border-subtle': theme.borderSubtle,
        '--border-strong': theme.borderStrong,
        '--shadow-soft': theme.shadowSoft,
        '--shadow-glow': theme.shadowGlow,
        '--shadow-glow-strong': theme.shadowGlowStrong,
        '--nav-background': theme.navBackground,
        '--nav-border': theme.navBorder,
        '--tab-active': theme.tabActive,
        '--tab-inactive': theme.tabInactive,
        '--button-primary-bg': theme.buttonPrimaryBg,
        '--button-primary-text': theme.buttonPrimaryText,
        '--button-ghost-border': theme.buttonGhostBorder,
        '--button-ghost-glow': theme.buttonGhostGlow,
        '--orb-color-a': theme.orbColorA,
        '--orb-color-b': theme.orbColorB,
        '--line-color': theme.lineColor,
        '--grid-color': theme.gridColor,
        '--backdrop-blur': theme.backdropBlur,
        '--panel-opacity': theme.panelOpacity,
        '--background-color': theme.backgroundColor,
        '--text-color': theme.textColor,
        '--text-color-light': theme.textSecondary,
        '--text-color-lighter': theme.textMuted,
        '--primary-color': theme.primaryColor,
        '--secondary-color': theme.secondaryColor,
        '--white': '#ffffff'
      }).forEach(([key, value]) => {
        root.style.setProperty(key, value);
      });

      root.dataset.theme = this.currentTheme;
      root.style.colorScheme = 'dark';
    },

    initTheme() {
      this.applyTheme();
    }
  }
});


import AktinsonHyperlegibleNextBold from './assets/fonts/AtkinsonHyperlegibleNext-Bold.woff2';
import AktinsonHyperlegibleNextBoldItalic from './assets/fonts/AtkinsonHyperlegibleNext-BoldItalic.woff2';
import AktinsonHyperlegibleNextExtraBold from './assets/fonts/AtkinsonHyperlegibleNext-ExtraBold.woff2';
import AktinsonHyperlegibleNextExtraBoldItalic from './assets/fonts/AtkinsonHyperlegibleNext-ExtraBoldItalic.woff2';
import AktinsonHyperlegibleNextExtraLight from './assets/fonts/AtkinsonHyperlegibleNext-ExtraLight.woff2';
import AktinsonHyperlegibleNextExtraLightItalic from './assets/fonts/AtkinsonHyperlegibleNext-ExtraLightItalic.woff2';
import AktinsonHyperlegibleNextLight from './assets/fonts/AtkinsonHyperlegibleNext-Light.woff2';
import AktinsonHyperlegibleNextLightItalic from './assets/fonts/AtkinsonHyperlegibleNext-LightItalic.woff2';
import AktinsonHyperlegibleNextMedium from './assets/fonts/AtkinsonHyperlegibleNext-Medium.woff2';
import AktinsonHyperlegibleNextMediumItalic from './assets/fonts/AtkinsonHyperlegibleNext-MediumItalic.woff2';
import AktinsonHyperlegibleNextRegular from './assets/fonts/AtkinsonHyperlegibleNext-Regular.woff2';
import AktinsonHyperlegibleNextRegularItalic from './assets/fonts/AtkinsonHyperlegibleNext-RegularItalic.woff2';
import AktinsonHyperlegibleNextSemiBold from './assets/fonts/AtkinsonHyperlegibleNext-SemiBold.woff2';
import AktinsonHyperlegibleNextSemiBoldItalic from './assets/fonts/AtkinsonHyperlegibleNext-SemiBoldItalic.woff2';

const fontWeightExtraLight = 200;
const fontWeightLight = 300;
const fontWeightRegular = 400;
const fontWeightMedium = 500;
const fontWeightSemiBold = 600;
const fontWeightBold = 700;
const fontWeightExtraBold = 800;

const fontFaces = [
  {
    fontFamily: 'Aktinson Hyperlegible',
    fontStyle: 'normal',
    fontDisplay: 'swap',
    fontWeight: fontWeightRegular,
    src: `url(${AktinsonHyperlegibleNextRegular}) format('woff2')`,
  },
  {
    fontFamily: 'Aktinson Hyperlegible',
    fontStyle: 'italic',
    fontDisplay: 'swap',
    fontWeight: fontWeightRegular,
    src: `url(${AktinsonHyperlegibleNextRegularItalic}) format('woff2')`,
  },
  {
    fontFamily: 'Aktinson Hyperlegible',
    fontStyle: 'normal',
    fontDisplay: 'swap',
    fontWeight: fontWeightBold,
    src: `url(${AktinsonHyperlegibleNextBold}) format('woff2')`,
  },
  {
    fontFamily: 'Aktinson Hyperlegible',
    fontStyle: 'italic',
    fontDisplay: 'swap',
    fontWeight: fontWeightBold,
    src: `url(${AktinsonHyperlegibleNextBoldItalic}) format('woff2')`,
  },
  {
    fontFamily: 'Aktinson Hyperlegible',
    fontStyle: 'normal',
    fontDisplay: 'swap',
    fontWeight: fontWeightExtraBold,
    src: `url(${AktinsonHyperlegibleNextExtraBold}) format('woff2')`,
  },
  {
    fontFamily: 'Aktinson Hyperlegible',
    fontStyle: 'italic',
    fontDisplay: 'swap',
    fontWeight: fontWeightExtraBold,
    src: `url(${AktinsonHyperlegibleNextExtraBoldItalic}) format('woff2')`,
  },
  {
    fontFamily: 'Aktinson Hyperlegible',
    fontStyle: 'normal',
    fontDisplay: 'swap',
    fontWeight: fontWeightExtraLight,
    src: `url(${AktinsonHyperlegibleNextExtraLight}) format('woff2')`,
  },
  {
    fontFamily: 'Aktinson Hyperlegible',
    fontStyle: 'italic',
    fontDisplay: 'swap',
    fontWeight: fontWeightExtraLight,
    src: `url(${AktinsonHyperlegibleNextExtraLightItalic}) format('woff2')`,
  },
  {
    fontFamily: 'Aktinson Hyperlegible',
    fontStyle: 'normal',
    fontDisplay: 'swap',
    fontWeight: fontWeightLight,
    src: `url(${AktinsonHyperlegibleNextLight}) format('woff2')`,
  },
  {
    fontFamily: 'Aktinson Hyperlegible',
    fontStyle: 'italic',
    fontDisplay: 'swap',
    fontWeight: fontWeightLight,
    src: `url(${AktinsonHyperlegibleNextLightItalic}) format('woff2')`,
  },
  {
    fontFamily: 'Aktinson Hyperlegible',
    fontStyle: 'normal',
    fontDisplay: 'swap',
    fontWeight: fontWeightMedium,
    src: `url(${AktinsonHyperlegibleNextMedium}) format('woff2')`,
  },
  {
    fontFamily: 'Aktinson Hyperlegible',
    fontStyle: 'italic',
    fontDisplay: 'swap',
    fontWeight: fontWeightMedium,
    src: `url(${AktinsonHyperlegibleNextMediumItalic}) format('woff2')`,
  },
  {
    fontFamily: 'Aktinson Hyperlegible',
    fontStyle: 'normal',
    fontDisplay: 'swap',
    fontWeight: fontWeightSemiBold,
    src: `url(${AktinsonHyperlegibleNextSemiBold}) format('woff2')`,
  },
  {
    fontFamily: 'Aktinson Hyperlegible',
    fontStyle: 'italic',
    fontDisplay: 'swap',
    fontWeight: fontWeightSemiBold,
    src: `url(${AktinsonHyperlegibleNextSemiBoldItalic}) format('woff2')`,
  },
];


const styleOverrides = fontFaces.reduce((acc, { fontFamily, fontStyle, fontDisplay, fontWeight, src }) => {
  acc += `
    @font-face {
      font-family: '${fontFamily}';
      font-style: ${fontStyle};
      font-display: ${fontDisplay};
      font-weight: ${fontWeight};
      src: ${src};
    }
  `;
  return acc;
}, '');


export default {
  typography: {
    fontFamily: 'Aktinson Hyperlegible, Roboto, sans-serif',
  },
  components: {
    MuiCssBaseline: {
      styleOverrides,
    },
  },
}
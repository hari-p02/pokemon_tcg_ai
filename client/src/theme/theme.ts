import { extendTheme } from '@chakra-ui/react';
import ButtonTheme from './buttonTheme';
import InputTheme from './inputTheme';
import colors from './colorTheme';

const theme = extendTheme({
  colors,
  components: {
    Button: ButtonTheme,
    Input: InputTheme,
  },
});

export default theme;

const ButtonTheme = {
  baseStyle: {
    _hover: {
      _disabled: null,
    },
    _active: {
      opacity: 0.7,
    },
    _disabled: {
      opacity: 0.7,
    },
    fontWeight: 700,
    borderRadius: '20px',
  },
  variants: {
    primary: {
      bg: 'gray.200',
      color: 'black',
    },
  },
  defaultProps: {
    variant: 'primary',
  },
};

export default ButtonTheme;

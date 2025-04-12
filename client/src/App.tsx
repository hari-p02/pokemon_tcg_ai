import { Box } from '@chakra-ui/react';
import McFlex from './McFlex/McFlex';

function App() {
  return (
    <Box
      id="AppWrapper"
      w="100%"
      h="100%"
      overflow="hidden"
      position="relative"
      bg="gray.100"
    >
      <McFlex>Test</McFlex>
    </Box>
  );
}

export default App;

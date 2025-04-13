import { Box, Button, Text, VStack } from '@chakra-ui/react';
import { motion } from 'framer-motion';

const MotionBox = motion(Box);

interface SlideProps {
  children: React.ReactNode;
  onNext: () => void;
  isLastSlide?: boolean;
}

const Slide = ({ children, onNext, isLastSlide = false }: SlideProps) => {
  return (
    <Box
      w="100vw"
      h="100vh"
      display="flex"
      alignItems="center"
      justifyContent="center"
      bg="linear-gradient(135deg, #1a202c 0%, #2d3748 100%)"
      position="relative"
      overflow="hidden"
    >
      <MotionBox
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: 'easeOut' }}
        w="100%"
        h="100%"
        display="flex"
        alignItems="center"
        justifyContent="center"
      >
        {children}
      </MotionBox>

      <Button
        position="absolute"
        bottom="40px"
        right="40px"
        bg="linear-gradient(135deg, #4299E1 0%, #3182CE 100%)"
        color="white"
        onClick={onNext}
        size="lg"
        fontWeight="900"
        fontFamily="'Press Start 2P', monospace"
        fontSize="16px"
        letterSpacing="1px"
        textTransform="uppercase"
        transition="all 0.2s"
        boxShadow="0 6px 0 #2C5282, 0 8px 12px rgba(0, 0, 0, 0.5)"
        border="3px solid #2C5282"
        borderRadius="12px"
        p="30px"
        _hover={{
          transform: 'translateY(-0.5px)',
          boxShadow: '0 8px 0 #2C5282, 0 12px 16px rgba(0, 0, 0, 0.4)',
          bg: 'linear-gradient(135deg, #63B3ED 0%, #4299E1 100%)',
        }}
        _active={{
          transform: 'translateY(2px)',
          boxShadow: '0 4px 0 #2C5282, 0 6px 8px rgba(0, 0, 0, 0.5)',
        }}
      >
        NEXT
      </Button>
    </Box>
  );
};

export default Slide;

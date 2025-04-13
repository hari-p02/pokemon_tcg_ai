import { Box, Button, Image, Text, VStack } from '@chakra-ui/react';
import { motion } from 'framer-motion';

const MotionBox = motion(Box);

interface HomePageProps {
  onNext: () => void;
}

const HomePage = ({ onNext }: HomePageProps) => {
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
      {/* Background Pokémon */}
      <MotionBox
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 1.2 }}
      >
        <MotionBox
          position="absolute"
          top="40%"
          left="20%"
          animate={{
            y: [0, 25, 0],
          }}
          transition={{
            duration: 4,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        >
          <Image
            src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/25.gif"
            alt="Pikachu"
            filter="brightness(0.8)"
            opacity="0.5"
            style={{ imageRendering: 'pixelated' }}
            w="180px"
          />
        </MotionBox>
      </MotionBox>

      <MotionBox
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 2.4 }}
      >
        <MotionBox
          position="absolute"
          top="70%"
          right="2%"
          animate={{
            y: [0, -25, 0],
          }}
          transition={{
            duration: 5,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        >
          <Image
            src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/6.gif"
            alt="Charizard"
            filter="brightness(0.8)"
            opacity="0.5"
            style={{ imageRendering: 'pixelated' }}
            w="220px"
          />
        </MotionBox>
      </MotionBox>

      <MotionBox
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 1.8 }}
      >
        <MotionBox
          position="absolute"
          top="10%"
          right="0%"
          animate={{
            y: [0, 20, 0],
          }}
          transition={{
            duration: 3.5,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        >
          <Image
            src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/150.gif"
            alt="Mewtwo"
            filter="brightness(0.8)"
            opacity="0.5"
            style={{ imageRendering: 'pixelated' }}
            w="300px"
          />
        </MotionBox>
      </MotionBox>

      <MotionBox
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 2.7 }}
      >
        <MotionBox
          position="absolute"
          top="70%"
          left="5%"
          animate={{
            y: [0, -20, 0],
          }}
          transition={{
            duration: 4.5,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        >
          <Image
            src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/3.gif"
            alt="Venusaur"
            filter="brightness(0.8)"
            opacity="0.5"
            style={{ imageRendering: 'pixelated' }}
            w="200px"
          />
        </MotionBox>
      </MotionBox>

      {/* Additional Pokémon */}
      <MotionBox
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 1.5 }}
      >
        <MotionBox
          position="absolute"
          top="45%"
          right="90%"
          animate={{
            y: [0, -15, 0],
          }}
          transition={{
            duration: 4.2,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        >
          <Image
            src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/151.gif"
            alt="Mew"
            filter="brightness(0.8)"
            opacity="0.5"
            style={{ imageRendering: 'pixelated' }}
            w="160px"
          />
        </MotionBox>
      </MotionBox>

      <MotionBox
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 2.1 }}
      >
        <MotionBox
          position="absolute"
          top="10%"
          right="25%"
          animate={{
            y: [0, -18, 0],
          }}
          transition={{
            duration: 4.8,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        >
          <Image
            src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/144.gif"
            alt="Articuno"
            filter="brightness(0.8)"
            opacity="0.5"
            style={{ imageRendering: 'pixelated' }}
            w="180px"
          />
        </MotionBox>
      </MotionBox>

      <MotionBox
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 2.9 }}
      >
        <MotionBox
          position="absolute"
          top="70%"
          left="25%"
          animate={{
            y: [0, 15, 0],
          }}
          transition={{
            duration: 3.2,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        >
          <Image
            src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/146.gif"
            alt="Moltres"
            filter="brightness(0.8)"
            opacity="0.5"
            style={{ imageRendering: 'pixelated' }}
            w="300px"
          />
        </MotionBox>
      </MotionBox>

      <MotionBox
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 1.7 }}
      >
        <MotionBox
          position="absolute"
          top="5%"
          left="25%"
          animate={{
            y: [0, -22, 0],
          }}
          transition={{
            duration: 4.6,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        >
          <Image
            src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/145.gif"
            alt="Zapdos"
            filter="brightness(0.8)"
            opacity="0.5"
            style={{ imageRendering: 'pixelated' }}
            w="180px"
          />
        </MotionBox>
      </MotionBox>

      <MotionBox
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 2.3 }}
      >
        <MotionBox
          position="absolute"
          top="40%"
          right="20%"
          animate={{
            y: [0, 16, 0],
          }}
          transition={{
            duration: 3.8,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        >
          <Image
            src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/143.gif"
            alt="Snorlax"
            filter="brightness(0.8)"
            opacity="0.5"
            style={{ imageRendering: 'pixelated' }}
            w="230px"
          />
        </MotionBox>
      </MotionBox>

      <MotionBox
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 2.6 }}
      >
        <MotionBox
          position="absolute"
          top="15%"
          left="45%"
          animate={{
            y: [0, -21, 0],
          }}
          transition={{
            duration: 4.7,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        >
          <Image
            src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/131.gif"
            alt="Lapras"
            filter="brightness(0.8)"
            opacity="0.5"
            style={{ imageRendering: 'pixelated' }}
            w="180px"
          />
        </MotionBox>
      </MotionBox>

      <MotionBox
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 1.9 }}
      >
        <MotionBox
          position="absolute"
          top="75%"
          right="35%"
          animate={{
            y: [0, 17, 0],
          }}
          transition={{
            duration: 3.6,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        >
          <Image
            src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/130.gif"
            alt="Gyarados"
            filter="brightness(0.8)"
            opacity="0.5"
            style={{ imageRendering: 'pixelated' }}
            w="200px"
          />
        </MotionBox>
      </MotionBox>

      <MotionBox
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 2.5 }}
      >
        <MotionBox
          position="absolute"
          top="5%"
          left="5%"
          animate={{
            y: [0, 20, 0],
          }}
          transition={{
            duration: 3.9,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        >
          <Image
            src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/149.gif"
            alt="Dragonite"
            filter="brightness(0.8)"
            opacity="0.5"
            style={{ imageRendering: 'pixelated' }}
            w="200px"
          />
        </MotionBox>
      </MotionBox>

      <MotionBox
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: 'easeOut', delay: 0.5 }}
      >
        <VStack spacing={2}>
          <Text
            fontFamily="'Press Start 2P', monospace"
            fontSize="50px"
            fontWeight="900"
            color="white"
            textAlign="center"
            textShadow="6px 6px 0 rgba(0, 0, 0, 0.5)"
            letterSpacing="3px"
            mb="40px"
          >
            pok
            <Text as="span" fontSize="50px">
              é
            </Text>
            play
            <Text as="span" fontSize="30px" color="#FFD700">
              .ai
            </Text>
          </Text>
          <Button
            bg="linear-gradient(135deg, #48BB78 0%, #2F855A 100%)"
            color="white"
            onClick={onNext}
            size="lg"
            fontWeight="900"
            fontFamily="'Press Start 2P', monospace"
            fontSize="16px"
            letterSpacing="1px"
            textTransform="uppercase"
            transition="all 0.2s"
            boxShadow="0 6px 0 #276749, 0 8px 12px rgba(0, 0, 0, 0.5)"
            border="3px solid #276749"
            borderRadius="12px"
            p="30px"
            _hover={{
              transform: 'translateY(-0.5px)',
              boxShadow: '0 8px 0 #276749, 0 12px 16px rgba(0, 0, 0, 0.4)',
              bg: 'linear-gradient(135deg, #68D391 0%, #38A169 100%)',
            }}
            _active={{
              transform: 'translateY(2px)',
              boxShadow: '0 4px 0 #276749, 0 6px 8px rgba(0, 0, 0, 0.5)',
            }}
          >
            GAME START
          </Button>
        </VStack>
      </MotionBox>
    </Box>
  );
};

export default HomePage;

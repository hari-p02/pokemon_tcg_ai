import { Box, Button, Text, VStack, useToast, Code } from '@chakra-ui/react';
import { useState, useRef, useEffect, useCallback } from 'react';
import { fetchGameState } from '../services/api';
import { flushSync } from 'react-dom';

interface TurnConsoleProps {
  onGameStateUpdated: () => void;
}

interface OutputLine {
  text: string;
  isDebug: boolean;
  id: number; // Add unique ID for better React rendering
}

const TurnConsole: React.FC<TurnConsoleProps> = ({ onGameStateUpdated }) => {
  const [outputLines, setOutputLines] = useState<OutputLine[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const outputRef = useRef<HTMLDivElement>(null);
  const lineIdCounter = useRef<number>(0);
  const toast = useToast();
  const eventSourceRef = useRef<EventSource | null>(null);

  // Force scroll to bottom whenever outputLines changes
  useEffect(() => {
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight;
    }
  }, [outputLines]);

  // Function to add a line with a unique ID
  const addOutputLine = useCallback((text: string, isDebug: boolean) => {
    const id = lineIdCounter.current++;
    // Use flushSync to force an immediate update
    flushSync(() => {
      setOutputLines((prevLines) => [...prevLines, { text, isDebug, id }]);
    });

    // Scroll immediately after update
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight;
    }
  }, []);

  // Cleanup function for event source
  useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, []);

  const handlePlayerTurn = async (playerNumber: 1 | 2) => {
    // Clean up any existing EventSource
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    setIsLoading(true);
    setOutputLines([]);
    lineIdCounter.current = 0;

    try {
      // addOutputLine(`Starting Player ${playerNumber} turn...`, false);

      // Use the more direct fetch API with streaming reader
      const response = await fetch(
        `http://localhost:8000/player${playerNumber}/turn`
      );

      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }

      if (!response.body) {
        throw new Error('Response has no body');
      }

      // Set up the reader
      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      // Read chunks as they arrive
      let buffer = '';

      // Process the stream
      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          console.log('Stream complete');
          break;
        }

        // Decode the chunk and add it to the buffer
        const text = decoder.decode(value, { stream: true });
        buffer += text;

        // Process any complete SSE messages in the buffer
        let startIndex = 0;
        let endIndex;

        while ((endIndex = buffer.indexOf('\n\n', startIndex)) !== -1) {
          const message = buffer.substring(startIndex, endIndex);
          const dataMatch = message.match(/^data: (.*)$/m);

          if (dataMatch) {
            const data = dataMatch[1];
            console.log('Processing message:', data);

            // Check if it's the close event
            if (message.includes('event: close')) {
              console.log('Close event received');
              // Handle close event
              addOutputLine('Stream closed by server', false);

              // Fetch updated state
              try {
                addOutputLine('Fetching updated game state...', false);
                await fetchGameState();
                onGameStateUpdated();
                setIsLoading(false);
                addOutputLine('State updated successfully', false);
              } catch (error) {
                console.error('Error fetching final state:', error);
                addOutputLine(`Error fetching state: ${error}`, false);
                setIsLoading(false);
              }
            } else {
              // Regular data message
              const isDebug = data.startsWith('[DEBUG]');
              const displayText = isDebug ? data.substring(7).trim() : data;

              if (displayText) {
                addOutputLine(displayText, isDebug);
              }
            }
          }

          startIndex = endIndex + 2;
        }

        // Keep any incomplete message in the buffer
        buffer = buffer.substring(startIndex);
      }

      // Clean up
      setIsLoading(false);

      toast({
        title: 'Turn completed',
        status: 'success',
        duration: 2000,
        isClosable: true,
      });
    } catch (error) {
      console.error('Error during turn:', error);
      addOutputLine(`Error: ${error}`, false);
      setIsLoading(false);

      toast({
        title: 'Error',
        description: 'Failed to process turn',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  return (
    <VStack
      spacing={4}
      p={4}
      border="1px solid"
      borderColor="gray.200"
      borderRadius="md"
      bg="white"
      width="100%"
    >
      <Text fontSize="lg" fontWeight="bold" alignSelf="flex-start">
        Turn Console{' '}
        {isLoading && (
          <Text as="span" color="orange.500">
            (Processing...)
          </Text>
        )}
      </Text>

      <Box
        ref={outputRef}
        p={3}
        bg="gray.900"
        borderRadius="md"
        width="100%"
        height="400px"
        overflowY="auto"
        fontFamily="monospace"
        whiteSpace="pre-wrap"
        color="white"
      >
        {outputLines.length === 0 ? (
          <Text color="gray.400">
            No output yet. Start a turn to see results.
          </Text>
        ) : (
          outputLines.map((line) => (
            <Box
              key={line.id}
              color={line.isDebug ? 'green.300' : 'white'}
              fontSize={line.isDebug ? 'xs' : 'sm'}
              mb={1}
            >
              {line.text}
            </Box>
          ))
        )}
      </Box>

      <Box display="flex" width="100%" justifyContent="space-between">
        <Button
          colorScheme="blue"
          onClick={() => handlePlayerTurn(1)}
          isDisabled={isLoading}
          width="48%"
        >
          Player 1 Turn
        </Button>
        <Button
          colorScheme="green"
          onClick={() => handlePlayerTurn(2)}
          isDisabled={isLoading}
          width="48%"
        >
          Player 2 Turn
        </Button>
      </Box>
    </VStack>
  );
};

export default TurnConsole;

import { Text } from '@chakra-ui/core';
import ReactCountdown, { zeroPad } from 'react-countdown';
import { If } from '~/components';
import { useColorValue } from '~/context';

import type { ICountdown, IRenderer } from './types';

const Renderer = (props: IRenderer) => {
  const { hours, minutes, seconds, completed, text } = props;
  let time = [zeroPad(seconds)];
  minutes !== 0 && time.unshift(zeroPad(minutes));
  hours !== 0 && time.unshift(zeroPad(hours));
  const bg = useColorValue('black', 'white');
  return (
    <>
      <If condition={completed}>
        <Text fontSize="xs" />
      </If>
      <If condition={!completed}>
        <Text fontSize="xs" color="gray.500">
          {text}
          <Text as="span" fontSize="xs" color={bg}>
            {time.join(':')}
          </Text>
        </Text>
      </If>
    </>
  );
};

export const Countdown = (props: ICountdown) => {
  const { timeout, text } = props;
  const then = timeout * 1000;
  return (
    <ReactCountdown
      date={Date.now() + then}
      daysInHours
      renderer={renderProps => <Renderer {...renderProps} text={text} />}
    />
  );
};
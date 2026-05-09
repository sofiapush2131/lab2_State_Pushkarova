from __future__ import annotations
from abc import ABC, abstractmethod


class State(ABC):

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def check_self(self, char: str) -> bool:
        """
        function checks whether occured character is handled by current ctate
        """
        pass

    def check_next(self, next_char: str) -> State | Exception:
        for state in self.next_states:
            if state.check_self(next_char):
                return state
        raise NotImplementedError("rejected string")


class StartState(State):
    next_states: list[State] = []

    def __init__(self):
        super().__init__()

    def check_self(self, char):
        return super().check_self(char)


class TerminationState(State):
    # pass  # Implement
    def __init__(self) -> None:
        self.next_states = []

    def check_self(self, char: str) -> bool:
        return False


class DotState(State):
    """
    state for . character (any character accepted)
    """

    next_states: list[State] = []

    def __init__(self):
        self.next_states = []
        super().__init__()

    def check_self(self, char: str):
        return True


class AsciiState(State):
    """
    state for alphabet letters or numbers
    """

    next_states: list[State] = []
    curr_sym = ""

    def __init__(self, symbol: str) -> None:
        # pass  # Implement
        self.next_states = []
        self.curr_sym = symbol

    def check_self(self, curr_char: str) -> State | Exception:
        # pass  # Implement
        return self.curr_sym == curr_char


class StarState(State):

    next_states: list[State] = []

    def __init__(self, checking_state: State):
        # pass  # Implement
        self.next_states = []
        self.checking_state = checking_state

    def check_self(self, char):
        for state in self.next_states:
            if state.check_self(char):
                return True
        return self.checking_state.check_self(char)


class PlusState(State):
    next_states: list[State] = []

    def __init__(self, checking_state: State):
        # pass  # Implement
        self.next_states = []
        self.checking_state = checking_state

    def check_self(self, char):
        # pass  # Implement
        return self.checking_state.check_self(char)


class RegexFSM:
    curr_state: State = StartState()

    def __init__(self, regex_expr: str) -> None:

        prev_state = self.curr_state
        tmp_next_state = self.curr_state

        for char in regex_expr:
            tmp_next_state = self.__init_next_state(char, prev_state, tmp_next_state)
            prev_state.next_states.append(tmp_next_state)

    def __init_next_state(
        self, next_token: str, prev_state: State, tmp_next_state: State
    ) -> State:
        new_state = None

        match next_token:
            case next_token if next_token == ".":
                new_state = DotState()
            case next_token if next_token == "*":
                new_state = StarState(tmp_next_state)
                # here you have to think, how to do it.
                if tmp_next_state in prev_state.next_states:
                    prev_state.next_states.remove(tmp_next_state)

            case next_token if next_token == "+":
                # pass  # Implement
                new_state = PlusState(tmp_next_state)

                if tmp_next_state in prev_state.next_states:
                    prev_state.next_states.remove(tmp_next_state)

            case next_token if next_token.isascii():
                new_state = AsciiState(next_token)

            case _:
                raise AttributeError("Character is not supported")

        return new_state

    def check_string(self, text: str):
        # pass  # Implement
        stt_pipeline = self.curr_state.next_states

        def dfs(state_idx, ch_idx):
            if state_idx == len(stt_pipeline):
                return ch_idx == len(text)

            curr_state = stt_pipeline[state_idx]

            if isinstance(curr_state, StarState):
                if dfs(state_idx + 1, ch_idx):
                    return True

                if ch_idx < len(text) and curr_state.check_self(text[ch_idx]):
                    if dfs(state_idx, ch_idx + 1):
                        return True
                return False

            if isinstance(curr_state, PlusState):
                if ch_idx < len(text) and curr_state.check_self(text[ch_idx]):
                    if dfs(state_idx + 1, ch_idx + 1):
                        return True
                    temp_star = StarState(curr_state.checking_state)
                    stt_pipeline[state_idx] = temp_star
                    res = dfs(state_idx, ch_idx + 1)
                    stt_pipeline[state_idx] = curr_state
                    if res:
                        return True
                return False

            if ch_idx < len(text) and curr_state.check_self(text[ch_idx]):
                return dfs(state_idx + 1, ch_idx + 1)

            return False

        return dfs(0, 0)


if __name__ == "__main__":
    regex_pattern = "a*4.+hi"

    regex_compiled = RegexFSM(regex_pattern)

    print(regex_compiled.check_string("aaaaaa4uhi"))  # True
    print(regex_compiled.check_string("4uhi"))  # True
    print(regex_compiled.check_string("meow"))  # False

def list_to_int(list):
  strings = [str(item) for item in list]

  joined_strings = "".join(strings)
  return int(joined_strings)

def all_combinations(colors, spots):
    all = []
    
    for i in range(colors**spots):
      number = i
      ans = [0 for k in range(spots)]
      ans_index = len(ans) - 1
      
      while number > 0:
        ans[ans_index] = (number % colors)
        number //= colors
        ans_index -= 1

      for i in range(spots):
        ans[i] += 1

      all.append(ans)

    return all

def calculate_score(secret, guess):
  exact = 0
  temp_exact = []
  for i in range(len(secret)):
    if secret[i] == guess[i]:
      temp_exact.append(secret[i])

  exact = len(temp_exact)

  inexact = 0
  secret_count = {}
  guess_count = {}
  for i in range(len(secret)):
    if secret[i] not in secret_count:
      secret_count[secret[i]] = 1
    else:
      secret_count[secret[i]] += 1

    if guess[i] not in guess_count:
      guess_count[guess[i]] = 1
    else:
      guess_count[guess[i]] += 1

  for color in secret_count:
    if color in guess_count:
      if color not in temp_exact:
        inexact += min(secret_count[color], guess_count[color])

  return (exact, inexact)

def minimax(knuth_codes, havent_guessed):
  num_of_all_feedback = {}
  scores = {}
  guess_codes = []
  
  for code in havent_guessed:
    for code_to_crack in knuth_codes:
      feedback = calculate_score(code_to_crack, code)

      if feedback not in num_of_all_feedback:
        num_of_all_feedback[feedback] = 1
      else:
        num_of_all_feedback[feedback] += 1

    maximum = max(num_of_all_feedback, key=num_of_all_feedback.get)
    scores[list_to_int(code)] = num_of_all_feedback[maximum]

  minimum = min(scores, key=scores.get)

  for code in havent_guessed:
    if scores[list_to_int(code)] == scores[minimum]:
      guess_codes.append(code)

  return guess_codes

def get_code(knuth_codes, havent_guessed):
  guess_codes = minimax(knuth_codes, havent_guessed)
  code = get_guess_code_from_list(knuth_codes, guess_codes)

  havent_guessed.remove(code)

  return code

def get_guess_code_from_list(knuth_codes, guess_codes):
#   print(guess_codes)
  for code in knuth_codes:
    if code in guess_codes:
      return code

  return guess_codes[0]

def prune_list(last_guess, feedback, knuth_codes):
  for code in knuth_codes:
    retrieved_feedback = calculate_score(code, last_guess)

    if retrieved_feedback != feedback:
      knuth_codes.remove(code)

def mastermind(colors, spots):
  total_codes = all_combinations(colors, spots)
  knuth_codes = total_codes
  havent_guessed = total_codes

  secret_int = int(input("Enter a combination of four numbers from 1-8 (ie: 1548): \n"))

  if len(str(secret_int)) == 4:

    secret = list(map(int, str(secret_int)))
    
    guesses = 0
    feedback = None
    
    while feedback != (4,0):
      if guesses == 0:
        guess = [1,1,2,2]
        feedback = calculate_score(secret, [1,1,2,2])
      else:
        guess = get_code(knuth_codes, havent_guessed)
        feedback = calculate_score(secret, guess)
        
      guesses += 1

      print(f"Guess {guesses}: {guess} --> {feedback}")

      if feedback == (4,0):
        break
      else:
        prune_list(guess, feedback, knuth_codes)

    return f"Guesses Made: {guesses}"

  else:
    return "Please enter 4 numbers"

print(mastermind(8, 4))
input("Press enter to close")
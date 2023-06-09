levenshtein_distance = """
    function(query, str) {
        var matrix = [];
        var i, j;
        for (i = 0; i <= query.length; i++) {
            matrix[i] = [i];
        }
        for (j = 1; j <= str.length; j++) {
            matrix[0][j] = j;
        }
        for (i = 1; i <= query.length; i++) {
            for (j = 1; j <= str.length; j++) {
                if (query[i - 1] === str[j - 1]) {
                    matrix[i][j] = matrix[i - 1][j - 1];
                } else {
                    matrix[i][j] = Math.min(
                        matrix[i - 1][j - 1] + 1,
                        matrix[i][j - 1] + 1,
                        matrix[i - 1][j] + 1
                    );
                }
            }
        }
        return matrix[query.length][str.length];
    }
"""
# TODO: Add the indexes in queryCounter and stringCounter and then use the sum() to get the number of chars
string_char_distance = """
function characterMatchDistance(inputQuery, inputString) {
  const query = inputQuery.toLowerCase()
  const string = inputString.toLowerCase()
  const queryCounter = {};
  const stringCounter = {};

  // Count the characters in the query string
  for (const char of query) {
    queryCounter[char] = (queryCounter[char] || 0) + 1;
  }

  // Count the characters in the string
  for (const char of string) {
    stringCounter[char] = (stringCounter[char] || 0) + 1;
  }

  let matchCount = 0;
  const matchingPositions = [];

  // Iterate over the shorter string for efficient character matching
  const shorterString = query.length <= string.length ? query : string;

  for (let i = 0; i < shorterString.length; i++) {
    const char = shorterString[i];

    if (queryCounter[char] && stringCounter[char]) {
      const minFrequency = Math.min(queryCounter[char], stringCounter[char]);
      matchCount += minFrequency;

      const matchPos = string.indexOf(char)

      if (matchPos !== -1) matchingPositions.push(matchPos)
    }
  }

  return { matchCount, matchingPositions };
}
"""

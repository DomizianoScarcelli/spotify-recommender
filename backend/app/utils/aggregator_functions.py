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
# TODO: Maybe make it more efficient
string_char_distance = """
function characterMatchDistance(inputQuery, inputString) {
    const query = inputQuery.toLowerCase();
    const string = inputString.toLowerCase();
    const chars = query.split("")
    let matchingPositions = []
    for (let char of chars) {
        const occurrencies = query.split(char).length - 1
        let index = string.indexOf(char);
        let howMany = 0
        while (index >= 0 && howMany < occurrencies) {
            if (index !== -1) matchingPositions.push(index)
            index = string.indexOf(char, index + 1);
            howMany += 1
        }

    }
    return {
        matchCount: matchingPositions.length,
        matchingPositions
    };
}
"""

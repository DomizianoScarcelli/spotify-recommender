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

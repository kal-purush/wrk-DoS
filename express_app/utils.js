function genstr(len, chr) {
    var result = "";
    for (let i = 0; i <= len; i++) {
      result = result + chr;
    }
    return result;
}
  
function measureTime(f, print) {
    var start = process.hrtime();
    f();
    var end = process.hrtime(start);
    // if (print === false) {
  
    // } else {
    //     console.info("Execution time (hr): %ds %dms", end[0], end[1] / 1000000);
    // }
    return end;
}

module.exports.genstr = genstr;
module.exports.measureTime = measureTime;
  
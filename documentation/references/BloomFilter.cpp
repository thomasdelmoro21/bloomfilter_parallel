#include "BloomFilter.h"

BloomFilter::BloomFilter(double fpr) : fpr(fpr), size(0), nHashes(0), bits(nullptr) {}


void BloomFilter::reset() {
    delete[] this->bits;
    this->size = 0;
    this->nHashes = 0;
}

void BloomFilter::initialize(std::size_t nItems) {
    reset();
    this->size = static_cast<int>(std::ceil(-(nItems * std::log(fpr)) / (std::log(2) * std::log(2))));
    this->nHashes = static_cast<int>(std::ceil((size / nItems) * std::log(2)));
    this->bits = new bool[this->size];
#pragma omp parallel for default(none) shared(bits) firstprivate(size)
    for(std::size_t i=0; i < this->size; i++)
        this->bits[i] = false;
}

double BloomFilter::sequentialSetup(std::string items[], std::size_t nItems) {
    initialize(nItems);
    double start = omp_get_wtime();
    for(std::size_t i=0; i < nItems; i++)
        add(items[i]);
    return omp_get_wtime() - start;
}

double BloomFilter::parallelSetup(std::string items[], std::size_t nItems) {
    initialize(nItems);
    double start = omp_get_wtime();
#pragma omp parallel for default(none) shared(bits, items) firstprivate(nItems, nHashes)
    for(std::size_t i=0; i < nItems; i++)
        add(items[i]);
    return omp_get_wtime() - start;
}

void BloomFilter::add(const std::string& items) {
    MultiHashes mh(this->size, items);
    for(std::size_t i=0; i < nHashes; i++)
        this->bits[mh()] = true;
}

int BloomFilter::sequentialFilterAll(std::string items[], size_t nItems) {
    int error = 0;
    for(std::size_t i=0; i < nItems; i++)
        if(filter(items[i]))
            error++;
    return error;
}

int BloomFilter::parallelFilterAll(std::string items[], size_t nItems) {
    int error = 0;
#pragma omp parallel for default(none) shared(items, error) firstprivate(nItems)
    for(std::size_t i=0; i < nItems; i++)
        if(filter(items[i]))
            error++;
    return error;
}

bool BloomFilter::filter(const std::string& email) {
    MultiHashes mh(this->size, email);
    for(std::size_t i=0; i < nHashes; i++)
        if(!this->bits[mh()]) return false; // SPAM = 0
    return true; // VALID = 1
}


BloomFilter::~BloomFilter() {
    this->reset();
}












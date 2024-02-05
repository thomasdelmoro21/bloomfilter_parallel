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
#pragma omp parallel default(none) shared(bits, items) firstprivate(nItems, nHashes)
    {
#pragma omp for
        for(std::size_t i=0; i < nItems; i++) {
            MultiHashes mh(this->size, items[i]);
            for (std::size_t h = 0; h < nHashes; h++) {
                std::size_t index = mh();
#pragma omp critical
                this->bits[index] = true;
            }
        }
    }
#pragma omp barrier
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

int BloomFilter::parallelFilterAll1(std::string items[], size_t nItems) {
    int error = 0;
#pragma omp parallel default(none) shared(items, error) firstprivate(nItems)
    {
#pragma omp for
        for (std::size_t i = 0; i < nItems; i++) {
            if (filter(items[i]))
#pragma omp atomic
                error++;
        }
    }
    return error;
}

int BloomFilter::parallelFilterAll2(std::string items[], size_t nItems) {
    int error = 0;
    int threadError = 0;
#pragma omp parallel default(none) shared(items, error) firstprivate(nItems, threadError)
    {
#pragma omp for
        for (std::size_t i = 0; i < nItems; i++) {
            if (filter(items[i]))
                threadError++;
        }
#pragma omp critical
        error += threadError;
    }
#pragma omp barrier
    return error;
}

bool BloomFilter::filter(const std::string& email) {
    MultiHashes mh(this->size, email);
    for(std::size_t i=0; i < nHashes; i++)
        if(!this->bits[mh()]) return false; // SPAM
    return true; // VALID
}


BloomFilter::~BloomFilter() {
    this->reset();
}

bool *BloomFilter::getBits() const {
    return bits;
}











